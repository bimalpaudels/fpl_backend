import enum
import time
import json
from datetime import datetime

import redis
import requests
from db_config import db_connection, pool
from utils import validated_required_attributes, filtered_players_details, player_history_mock_data
from typing import Tuple, Optional
from psycopg.rows import dict_row
from players.utils import calculate_hash


BASE_URL = 'https://fantasy.premierleague.com/api/'
TRACKED_FIELDS = ['now_cost', 'second_name']


# Redis Connection
r = redis.Redis(host='localhost', port=6379, db=0)


class ActionType(enum.Enum):
    """
    Enumeration of possible actions for player data from remote and local database.
    """
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    NO_ACTION = 'NO_ACTION'


def call_bootstrap_api():
    """
    The main api of Fantasy Premier League that returns everything.
    :return: Currently only returns the players data but others will be utilized in the future.
    """
    url = BASE_URL + 'bootstrap-static/'
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        players = response['elements']
        return players
    else:
        print("Something went wrong")
        return


def call_player_detail_api(player_id: int):
    """
    Get individual player details from remote api and return the history object.
    :param player_id: Player id from local database
    :return history: The history of individual player details for the season.
    """
    url = BASE_URL + f'element-summary/{player_id}/'
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        player_history = response['history']
        return player_history
    elif response.status_code == 429:
        print('Too many request')
        breakpoint()
        return


def get_players():
    """
    Function to get all players data calling the call_bootstrap_api function and insert into local database.
    :return: Currently only returns success message on console.
    """
    all_players_cache_key = "remote:players"
    players = r.get(all_players_cache_key)
    # print(players)
    if players:
        print("Data retrieved from cache")
        players = json.loads(players)
    else:
        print("Data fetched from remote and cached")
        players = call_bootstrap_api()
        r.setex(all_players_cache_key, 300, json.dumps(players))

    filtered_players_data = validated_required_attributes(players)
    upsert_players(filtered_players_data)
    # Clean players to only take data required.
    return True


def upsert_players(players):
    """
    Function called from get_players() to insert or update into local database
    :param players: List of players from get_players()
    :return: Print statement to console showing the count of the data manipulated.
    """
    inserted_count = 0
    updated_count = 0
    unchanged_count = 0

    with pool.connection() as conn:
        for player in players:
            action, changed_data = verify_player_exists(conn, player)

            if action == ActionType.CREATE:
                columns = ', '.join(player.keys())
                placeholders = ', '.join(['%s'] * len(player))
                values = tuple(player.values())
                query = f"INSERT INTO players ({columns})VALUES ({placeholders})"

                conn.execute(query, values)
                inserted_count += 1

            elif action == ActionType.UPDATE:
                set_clause = ", ".join(f"{key} = %s" for key in changed_data.keys())
                values = list(changed_data.values()) + [player['player_id']]
                query = f"UPDATE players SET {set_clause} WHERE player_id =%s"

                conn.execute(query, values)
                updated_count += 1
                # print(changed_data, player['player_id'], player['first_name'])

            else:
                unchanged_count += 1

    print(f"New Players: {inserted_count}, Updated: {updated_count}, Unchanged: {unchanged_count}")


def verify_player_exists(conn, player_detail) -> Tuple[ActionType, Optional[dict]]:

    # connection = db_connection()
    player_id = player_detail['player_id']
    hash_query = """SELECT hash_value FROM players WHERE player_id =%s"""
    full_query = """SELECT * FROM players WHERE player_id =%s"""

    with conn.cursor(row_factory=dict_row) as cursor:
        record = cursor.execute(hash_query, (player_id,)).fetchone()

        if record is None:
            return ActionType.CREATE, None

        if player_detail['hash_value'] == record['hash_value']:
            return ActionType.NO_ACTION, None

        record = cursor.execute(full_query, (player_id,)).fetchone()

        changed_values = {}

        for key, value in player_detail.items():
            # print(key, value, record.get(key))
            if value != record.get(key):
                print(key, value, record.get(key))
                changed_values[key] = value

        return ActionType.UPDATE, changed_values


def get_player_stats_by_gw():
    """
    Stats of every player in a particular game week. First need to get all players ID and then loop through the player
    detail api. First get the history data. Currently not available so mocking it in utils.
    :return:
    """
    query = """SELECT json_agg(player_id) FROM players"""

    with db_connection() as conn:
        results = conn.execute(query).fetchone()
    player_ids = results[0]
    for i in range(0, len(player_ids),  60):
        chunk = player_ids[i:i+60]
        for player_id in chunk:
            data = call_player_detail_api(player_id)

            # data and  player_ids will be used in the future
            # history = player_history_mock_data(player_id)
            filtered_player_data = filtered_players_details(data)
            upsert_player_stats_by_gw(filtered_player_data)
            time.sleep(1)
        print("Waiting 60 seconds...")
        time.sleep(60)
    return True


def upsert_player_stats_by_gw(player_data):
    inserted_count = 0
    updated_count = 0
    unchanged_count = 0
    player = ""

    for data in player_data:
        player = data['player_id']
        action_type, changed_data = verify_player_gw_exists(data)

        if action_type == ActionType.CREATE:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            values = tuple(data.values())
            query = f"INSERT INTO players_detail ({columns})VALUES ({placeholders})"
            with db_connection() as conn:
                conn.execute(query, values)
            inserted_count += 1

        elif action_type == ActionType.UPDATE:
            set_clause = ", ".join(f"{key} = %s" for key in changed_data.keys())
            values = list(changed_data.values()) + [data['player_id']] + [data['game_week']]
            query = f"UPDATE players_detail SET {set_clause} WHERE player_id =%s AND game_week =%s"
            with db_connection() as conn:
                conn.execute(query, values)
            updated_count += 1

        else:
            unchanged_count += 1

    if inserted_count != 0 or updated_count != 0:
        print(f"{player} -> New gw: {inserted_count}, updated: {updated_count}, unchanged: {unchanged_count}")


def verify_player_gw_exists(player_data) -> Tuple[ActionType, Optional[dict]]:
    player_id = player_data.get("player_id")
    game_week = player_data.get("game_week")

    query = """SELECT * FROM players_detail WHERE player_id =%s AND game_week =%s"""
    with db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            data = cursor.execute(query, (player_id, game_week)).fetchone()

    if data is None:
        return ActionType.CREATE, None

    changed_values = {}

    for key, value in player_data.items():

        if value != data.get(key):
            changed_values[key] = value

    if changed_values:
        return ActionType.UPDATE, changed_values

    return ActionType.NO_ACTION, None


if __name__ == "__main__":
    try:
        start_time = datetime.now()
        if get_players():
            print("Successfully loaded players.")
        # if get_player_stats_by_gw():
        #     print("Successfully loaded individual gw data.")
        print("Scripts executed!!!")
        end_time = datetime.now()
        print(f"Script execution time: " + str(end_time - start_time))
    except Exception as e:
        print(e)



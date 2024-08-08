import enum
import requests
from db_config import db_connection
from utils import filter_required_attributes, filtered_players_details, player_history_mock_data
from typing import Tuple, Optional
from psycopg.rows import dict_row

BASE_URL = 'https://fantasy.premierleague.com/api/'
TRACKED_FIELDS = ['now_cost', 'second_name']


class ActionType(enum.Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    NO_ACTION = 'NO_ACTION'


def get_player_detail_api(player_id: int):
    url = BASE_URL + f'element-summary/{player_id}/'
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        player_history = response['history']
        return player_history
    elif response.status_code == 429:
        print('Too many request')
        breakpoint()


def get_bootstrap_api():
    """
    The main api of Fantasy Premier League that returns everything. The response is separated into players and
    their respective teams.
    :return: Response object of the bootstrap-static api
    """
    response = requests.get(BASE_URL+'bootstrap-static/').json()

    # Separate players
    players = response['elements']
    filtered_players_data = filter_required_attributes(players)
    upsert_players(filtered_players_data)
    # Clean players to only take data required.
    return filtered_players_data


def upsert_players(players):
    # Use players ID to check if the player exists
    # If player matching the id doesn't exist, insert operation
    # If player matching the id exists, compare the data
    # If there are changes, UPDATE else leave it as it is.
    inserted_count = 0
    updated_count = 0
    unchanged_count = 0

    for player in players:
        action, changed_data = verify_player_exists(player)

        if action == ActionType.CREATE:
            columns = ', '.join(player.keys())
            placeholders = ', '.join(['%s'] * len(player))
            values = tuple(player.values())
            query = f"INSERT INTO players ({columns})VALUES ({placeholders})"
            with db_connection() as conn:
                conn.execute(query, values)
            inserted_count += 1

        elif action == ActionType.UPDATE:
            set_clause = ", ".join(f"{key} = %s" for key in changed_data.keys())
            values = list(changed_data.values()) + [player['player_id']]
            query = f"UPDATE players SET {set_clause} WHERE player_id =%s"
            with db_connection() as conn:
                conn.execute(query, values)
            updated_count += 1

        else:
            unchanged_count += 1

    print(f"Inserted: {inserted_count}, updated: {updated_count}, unchanged: {unchanged_count}")


def verify_player_exists(player_detail) -> Tuple[ActionType, Optional[dict]]:

    connection = db_connection()
    player_id = player_detail['player_id']

    # Check if the player data exists in system
    query = """SELECT * FROM players WHERE player_id =%s"""
    with connection as conn:
        with conn.cursor(row_factory=dict_row) as cursor:

            record = cursor.execute(query, (player_id,)).fetchone()

    if record is None:
        return ActionType.CREATE, None

    changed_values = {}

    for field in TRACKED_FIELDS:
        remote_value = player_detail.get(field)
        local_value = record.get(field)

        if remote_value != local_value:
            changed_values[field] = remote_value

    if changed_values:
        return ActionType.UPDATE, changed_values

    return ActionType.NO_ACTION, None


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
    for player_id in range(1, 20):
        # data = get_player_detail_api(player_id)
        # data and  player_ids will be used in the future
        history = player_history_mock_data(player_id)
        filtered_player_data = filtered_players_details(history)
        upsert_player_stats_by_gw(filtered_player_data)
    # Mock will be replaced by actual API call later.


def upsert_player_stats_by_gw(player_data):
    inserted_count = 0
    updated_count = 0
    unchanged_count = 0

    for data in player_data:
        # Check if that gw data exists for that player (1, 182)
        action_type, changed_data = verify_player_gw_exists(data)
        # If it doesn't exist execute CREATE
        if action_type == ActionType.CREATE:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            values = tuple(data.values())
            query = f"INSERT INTO players_detail ({columns})VALUES ({placeholders})"
            with db_connection() as conn:
                conn.execute(query, values)
            inserted_count += 1
        # If it does exist check for changes
        # If there is changes, get the changes and update
        # Else just skip
        else:
            unchanged_count += 1
    print(f"Inserted: {inserted_count}, updated: {updated_count}, unchanged: {unchanged_count}")


def verify_player_gw_exists(player_data) -> Tuple[ActionType, Optional[dict]]:
    player_id = player_data.get("player_id")
    game_week = player_data.get("game_week")

    query = """SELECT * FROM players_detail WHERE player_id =%s AND game_week =%s"""
    with db_connection() as conn:
        data = conn.execute(query, (player_id, game_week)).fetchone()
    if data is None:
        return ActionType.CREATE, None
    else:
        return ActionType.NO_ACTION, None


if __name__ == "__main__":
    # get_bootstrap_api()
    get_player_stats_by_gw()

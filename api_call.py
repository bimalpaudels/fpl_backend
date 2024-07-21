import enum
import requests
from db_config import db_connection
from utils import filter_required_attributes
from typing import Tuple, Optional
from psycopg.rows import dict_row

BASE_URL = 'https://fantasy.premierleague.com/api/'
TRACKED_FIELDS = ['now_cost', 'second_name']


class ActionType(enum.Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    NO_ACTION = 'NO_ACTION'


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
            query = """INSERT INTO players (player_id, first_name, second_name, now_cost) VALUES (%s, %s, %s, %s)"""
            values = (player.get('player_id'), player.get('first_name'), player.get('second_name'), player.get('now_cost'))
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


if __name__ == "__main__":
    get_bootstrap_api()

import psycopg
import os
from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql+psycopg://postgres:postgres@localhost:5432/fpl_db")


def db_connection():
    """
    Making connection with Postgres using psycopg2
    :return: Connection object
    """
    connection = psycopg.connect(
        dbname=os.getenv("DB_NAME", "fpl_db"),
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
    )

    return connection


pool = ConnectionPool(conninfo=DATABASE_URL)


def create_players_table():
    """
    Create database table to save players data
    :return:
    """
    connection = db_connection()

    query = """
    CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    player_id INTEGER UNIQUE,
    first_name VARCHAR(100),
    second_name VARCHAR(100),
    now_cost INTEGER
    )"""

    with connection as conn:
        conn.execute(query)
        print("Executed")


if __name__ == "__main__":
    create_players_table()

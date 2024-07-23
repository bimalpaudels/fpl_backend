from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from db_config import pool
from psycopg.rows import dict_row

app = FastAPI()


class Player(BaseModel):
    first_name: str
    second_name: str
    now_cost: int
    player_id: int


@app.get("/")
async def root():
    return {"Root": "API"}


@app.get("/players/", response_model=List[Player])
async def get_players():
    query = "SELECT * FROM players"
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query)
            records = cur.fetchall()
    return records



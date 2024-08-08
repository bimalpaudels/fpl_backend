from http.client import HTTPException

from sqlalchemy.orm import Session
from players import models, schemas
from sqlalchemy import desc, asc


def get_players(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Player).offset(skip).limit(limit).all()


def get_players_details(db: Session, player_id: int):
    player = db.query(models.Player).get(player_id)
    return player


def get_top_5(db: Session, category: str):
    players = db.query(models.Player).order_by(desc(category)).limit(5)
    return players

from sqlalchemy.orm import Session
from players import models, schemas


def get_players(db: Session):
    return db.query(models.Player).all()


def get_players_details(db: Session, player_id: int):
    player = db.query(models.Player).get(player_id == player_id)
    # player_details = player.
    return player

from sqlalchemy.orm import Session
from players import models


def get_players(db: Session):
    return db.query(models.PlayerModel).all()

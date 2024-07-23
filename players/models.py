from sqlalchemy import Column, Integer, String

from .database import Base


class PlayerModel(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, unique=True)
    first_name = Column(String)
    second_name = Column(String)
    now_cost = Column(Integer)


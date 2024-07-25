from sqlalchemy import Column, Integer, String, UniqueConstraint

from .database import Base


class PlayerModel(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, unique=True)
    first_name = Column(String)
    second_name = Column(String)
    now_cost = Column(Integer)


class PlayersByGWModel(Base):
    __tablename__ = 'players_gw_detail'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    game_week = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    total_points = Column(Integer)

    __table_args__ = (
        UniqueConstraint('player_id', 'game_week'),
    )


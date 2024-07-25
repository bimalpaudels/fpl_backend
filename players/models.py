from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    second_name = Column(String)
    now_cost = Column(Integer)
    details = relationship('PlayersDetail', back_populates='player', cascade='all, delete-orphan')


class PlayersDetail(Base):
    __tablename__ = 'players_detail'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    game_week = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    total_points = Column(Integer)
    player = relationship("Player", back_populates="details")

    __table_args__ = (
        UniqueConstraint('player_id', 'game_week'),
    )


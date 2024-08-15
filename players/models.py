from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Float
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    second_name = Column(String)
    now_cost = Column(Integer)
    form = Column(Float, default=0)
    selected_by_percent = Column(Float, default=0.0)
    total_points = Column(Integer, default=0)
    minutes = Column(Integer, default=0)
    goals_scored = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    clean_sheets = Column(Integer, default=0)
    goals_conceded = Column(Integer, default=0)
    own_goals = Column(Integer, default=0)
    penalties_saved = Column(Integer, default=0)
    penalties_missed = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    bonus = Column(Integer, default=0)
    bps = Column(Integer, default=0)
    influence = Column(Float, default=0.0)
    creativity = Column(Float, default=0.0)
    threat = Column(Float, default=0.0)
    ict_index = Column(Float, default=0.0)
    starts = Column(Integer, default=0)
    expected_goals = Column(Float, default=0.0)
    expected_assists = Column(Float, default=0.0)
    expected_goals_conceded = Column(Float, default=0)
    expected_goals_involvement = Column(Float, default=0.0)
    expected_goals_per_90 = Column(Float, default=0)
    saves_per_90 = Column(Float, default=0)
    expected_assists_per_90 = Column(Float, default=0)
    expected_goals_involvements_per_90 = Column(Float, default=0)
    expected_goals_conceded_per_90 = Column(Float, default=0)
    goals_conceded_per_90 = Column(Float, default=0)
    points_per_game = Column(Float, default=0.0, nullable=True)

    position = Column(Integer, default=0)
    team = Column(Integer, default=1)
    web_name = Column(String)

    details = relationship('PlayersDetail', back_populates='player', cascade='all, delete-orphan')


class PlayersDetail(Base):
    __tablename__ = 'players_detail'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    game_week = Column(Integer)
    total_points = Column(Integer)
    minutes = Column(Integer)
    goals_scored = Column(Integer)
    assists = Column(Integer)
    clean_sheet = Column(Integer)
    goals_conceded = Column(Integer)
    own_goals = Column(Integer)
    penalties_saved = Column(Integer)
    penalties_missed = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    saves = Column(Integer)
    bonus = Column(Integer)
    bps = Column(Integer)
    influence = Column(Float)
    creativity = Column(Float)
    threat = Column(Float)
    ict_index = Column(Float)
    value = Column(Integer)
    selected = Column(Integer)
    transfers_in = Column(Integer)
    transfers_out = Column(Integer)

    player = relationship("Player", back_populates="details")

    __table_args__ = (
        UniqueConstraint('player_id', 'game_week'),
    )


from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PlayerSchema(BaseModel):
    first_name: str
    second_name: str
    now_cost: int
    player_id: int

    class Config:
        orm_mode = True


class PlayersDetailSchema(BaseModel):
    player_id: int
    game_week: int
    assists: int
    total_points: int
    minutes: int
    goals_scored: int
    assists: int
    clean_sheet: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int
    bps: int
    influence: float
    creativity: float
    threat: float
    ict_index: float
    value: int
    selected: int
    transfers_in: int
    transfers_out: int

    class Config:
        orm_mode = True


class PlayerDetailResponse(PlayerSchema):
    details: list[PlayersDetailSchema]

    class Config:
        orm_mode = True


class PlayerSelectedPercentageSchema(PlayerSchema):
    model_config = ConfigDict(from_attributes=True)

    selected_by_percent: Optional[float] = None
    total_points: Optional[int] = None
    expected_goals: Optional[float] = None
    expected_assists: Optional[float] = None
    threat: Optional[float] = None


class PlayerBasicSchema(PlayerSchema):
    model_config = ConfigDict(from_attributes=True)
    
    goals_scored: Optional[int] = None
    assists: Optional[int] = None
    own_goals: Optional[int] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None


class PlayerListResponseSchema(PlayerSchema):
    model_config = ConfigDict(from_attributes=True)

    minutes: int
    total_points: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PlayerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    second_name: str
    now_cost: int
    player_id: int


class PlayersDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: int = Field(..., alias='element')
    game_week: int = Field(..., alias='round')
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


class PlayerDetailResponse(PlayerSchema):
    model_config = ConfigDict(from_attributes=True)

    details: list[PlayersDetailSchema]


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


class PlayerCompleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: int = Field(..., alias='id')
    first_name: str
    second_name: str
    now_cost: int
    form: float
    selected_by_percent: float
    total_points: int
    minutes: int
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
    bps: int
    influence: float
    creativity: float
    threat: float
    ict_index: float
    starts: int
    expected_goals: float
    expected_assists: float
    expected_goals_conceded: float
    expected_goals_involvement: float = Field(..., alias='expected_goal_involvements')
    expected_goals_per_90: float
    saves_per_90: float
    expected_assists_per_90: float
    expected_goals_involvements_per_90: float = Field(..., alias='expected_goal_involvements_per_90')
    expected_goals_conceded_per_90: float
    goals_conceded_per_90: float
    points_per_game: float

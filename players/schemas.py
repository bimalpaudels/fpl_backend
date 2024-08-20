from pydantic import BaseModel, Field, ConfigDict, field_serializer, computed_field
from typing import Optional
from players.utils import player_position, get_team, calculate_hash


class PlayerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    second_name: str
    now_cost: int
    player_id: int
    web_name: str


class PlayersDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: int = Field(..., alias='element')
    game_week: int = Field(..., alias='round')
    assists: int
    total_points: int
    minutes: int
    goals_scored: int
    assists: int
    clean_sheet: int = Field(..., alias='clean_sheets')
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
    points_per_game: Optional[float] = None
    expected_goals_involvement: Optional[float] = None
    expected_goals_per_90: Optional[float] = None
    expected_assists_per_90: Optional[float] = None
    expected_goals_conceded: Optional[float] = None


class PlayerBasicSchema(PlayerSchema):
    model_config = ConfigDict(from_attributes=True)
    
    goals_scored: Optional[int] = None
    assists: Optional[int] = None
    own_goals: Optional[int] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None
    clean_sheets: Optional[int] = None
    minutes: Optional[int] = None


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

    position: int = Field(..., alias='element_type')
    team: int
    web_name: str

    @computed_field
    @property
    def hash_value(self) -> str:

        player_dict = self.model_dump(exclude={"hash_value"})
        return calculate_hash(player_dict)


class PlayerListResponseSchema(PlayerCompleteSchema):
    model_config = ConfigDict(from_attributes=True)
    player_id: int
    expected_goals_involvement: float
    expected_goals_involvements_per_90: float
    full_name: Optional[str] = None
    position: int
    team: int

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.second_name}"

    @field_serializer('full_name')
    def serialize_full_name(self, _) -> str:
        return self.get_full_name

    @field_serializer('position')
    def serialize_position(self, _) -> str:
        return player_position(self.position)

    @field_serializer('team')
    def serialize_team(self, _) -> str:
        return get_team(self.team)

    @field_serializer('now_cost')
    def serialize_now_cost(self, _) -> float:
        cost = self.now_cost
        return cost/10

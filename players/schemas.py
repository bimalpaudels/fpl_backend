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
    goals: int
    assists: int
    total_points: int

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

from pydantic import BaseModel


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

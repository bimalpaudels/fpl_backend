from pydantic import BaseModel


class PlayerSchema(BaseModel):
    first_name: str
    second_name: str
    now_cost: int
    player_id: int

    class Config:
        orm_mode = True

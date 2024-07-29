from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from players import models, crud, schemas
from players.database import SessionLocal, engine
from players.schemas import PlayerDetailResponse
from fastapi.responses import JSONResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"Root": "API"}


@app.get("/players", response_model=list[schemas.PlayerSchema])
def get_players(db: Session = Depends(get_db)):
    players = crud.get_players(db)
    return players


@app.get("/player/{player_id}", response_model=schemas.PlayerDetailResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_players_details(db=db, player_id=player_id)
    return player


@app.get("/player/{player_id_1}/{player_id_2}", response_model=list[schemas.PlayersDetailSchema])
def get_player_comp(player_id_1: int, player_id_2: int, db: Session = Depends(get_db)):
    player_1 = crud.get_players_details(db=db, player_id=player_id_1)
    player_2 = crud.get_players_details(db=db, player_id=player_id_2)
    return list(player_1) + list(player_2)


@app.get("/top-five", response_model=list[schemas.PlayerSelectedPercentageSchema])
def get_top_five_selected(category: str, db: Session = Depends(get_db)):
    expected_category = ['total_points', 'selected_by_percent', 'expected_goals']
    exclusion_fields = set(expected_category) - {category}
    if category not in expected_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category {category} not valid")
    players = crud.get_top_5(db=db, category=category)
    players_schemas = [
        schemas.PlayerSelectedPercentageSchema.model_validate(player).model_dump(exclude={field for field in exclusion_fields})
        for player in players
    ]
    return JSONResponse(content=players_schemas, status_code=status.HTTP_200_OK)

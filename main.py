from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from players import models, crud, schemas
from players.database import SessionLocal, engine


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





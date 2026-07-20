from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field

from sqlmodel import Session

from db import get_session
from models.game import Game
from models.play import Play
from services.game import create_game, get_game

class CreateOrGetGameResponse(BaseModel):

    id: int
    finished: bool
    winner: str | None
    draw: bool
    started_at: datetime
    finished_at: datetime | None
    plays: List[Play]



game_router = APIRouter( prefix = "/game", tags = ["game"])


#Game Routes
@game_router.get("/", response_model = CreateOrGetGameResponse, status_code = status.HTTP_201_CREATED )
@game_router.get("/{game_id}", response_model = CreateOrGetGameResponse, status_code = status.HTTP_200_OK )
def create_or_get_game(*, session: Session = Depends(get_session) , game_id: int = None ):
    
    if game_id:

        game = get_game( parent_session = session, game_id = game_id)

        return CreateOrGetGameResponse(**game.model_dump(), plays = game.plays)
    
    new_game = create_game( parent_session = session)
    
    return CreateOrGetGameResponse(**new_game.model_dump(), plays = new_game.plays)
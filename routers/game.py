
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlmodel import Session

from db import get_session
from models.game import Game
from services.game import create_game, get_game


game_router = APIRouter( prefix = "/game", tags = ["game"])


#Game Routes
@game_router.get("/")
@game_router.get("/{game_id}")
def create_or_get_game(*, session: Session = Depends(get_session) , game_id: int = None ):
    
    if game_id:

        game = get_game( parent_session = session, game_id = game_id)

        return game
    
    new_game = create_game( parent_session = session)
    
    return new_game
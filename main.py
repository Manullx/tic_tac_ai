import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from sqlmodel import Session

from db import session, Game, Play

#Functions
def create_game() -> int:

    game = Game( finished = False, started_at = datetime.now() )

    session.add( game )
    session.commit()

    return game.id


def create_play( game_id: int, state: list ) -> None:

    
    play = Play( game_id = game_id, state = state )
    
    session.add( play )
    session.commit()

    return


#FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)


#Routes
@app.get("/")
def index():

    return HTMLResponse( open("src/index.html").read(), status_code = 200, media_type = "text/html" )


@app.get("/game")
def game():
    
    game_id = create_game()
    
    return JSONResponse( { "game_id": game_id }, status_code = 200 )


@app.post("/play")
def play( play: Play ):
    
    game_id, state, id = play.model_dump().values()
    
    create_play( game_id, state )

    return JSONResponse({ 'row': random.randint( 1, 3 ), 'col': random.randint(1, 3) })
import random
from typing import List
from datetime import datetime
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Column, JSON, String, Field, SQLModel, Session, create_engine


#Models
class Game( SQLModel, table = True ):

    id: int | None = Field( default = None, primary_key = True )
    finished: bool
    started_at:  datetime
    finished_at: datetime | None


class Play( SQLModel, table = True ):

    game_id: int = Field( foreign_key = "game.id" )
    id: int | None = Field( default = None, primary_key = True )
    state: List[ str ] = Field( sa_column = Column( JSON ) )


#Classes
class GameState( BaseModel ):

    state: list


#Functions
def create_game() -> int:

    game = Game( finished = False, started_at = datetime.now() )

    session = Session( engine )

    session.add( game )

    session.commit()

    return game.id
    

#Execution

#DB
db_name = "db.sqlite"
db_uri = f"sqlite:///{db_name}"

engine = create_engine( db_uri, echo = True )

SQLModel.metadata.create_all( engine )

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


@app.post("/square")
async def square( game_state: GameState ):
    
    req_body = game_state.model_dump()
    state = req_body['state']


    return JSONResponse({ 'row': random.randint( 1, 3 ), 'col': random.randint(1, 3) })
import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from sqlmodel import Session, SQLModel, select

from db import engine, Game, Play
from rl.agent import define_agent_play
from rl.enviroment import evaluate_game_state


#Schemas
class PlayRequest( SQLModel ):

    game_id: int
    row: int
    col: int


#Functions
def create_game() -> int:

    with Session( engine ) as session:

        game = Game( finished = False, started_at = datetime.now() )

        session.add( game )
        session.commit()

        return game.id


def create_play( session: Session, game: Game, player: str, row: int, col: int ) -> None:

    play = Play( game_id = game.id, play_n = len( game.plays ), player = player, row = row, col = col, reward = 0 )

    session.add( play )
    session.commit()
    session.refresh( game )

    return


def verify_win( game: Game ) -> str | None:

    game_state = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    for p in game.plays:
        
        game_state[p.row][p.col] = p.player
        
    #Verify Lines
    for row in game_state:
        
        if None in row:
            continue
        
        if len( row_set := set(row) ) == 1:

            return row_set.pop()
    
    #Verify Cols
    for col_i in range(0, 3):
        
        col = [ row[col_i] for row in game_state  ]
        
        if None in col:
            continue
        
        if len( col_set := set(col) ) == 1:

            return col_set.pop()
    
    # #Verify Diagonals
    first_diagonal = [ game_state[ij][ij] for ij in range(0, 3) ]
    second_diagonal = [ game_state[ij][2 - ij] for ij in range(2, -1, -1) ]
    if len( first_diagonal_set := set(first_diagonal) ) == 1:

            return first_diagonal_set.pop()
    
    if len( second_diagonal_set := set(second_diagonal) ) == 1:

            return second_diagonal_set.pop()
    
    return None
    

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
    
    game_id: int = create_game()
    
    return JSONResponse( { "game_id": game_id }, status_code = 200 )


@app.post("/play")
def play( play: PlayRequest ):
    
    game_id = play.game_id
    player_row = play.row
    player_col = play.col

    with Session( engine ) as session:

        query = select( Game ).where( Game.id == game_id)
        result = session.exec( query )
        game = result.first()
        
        create_play( session, game, player = "X", row = player_row, col = player_col )

        if winner := verify_win( game ):
            
            game.finished = True
            game.finished_at = datetime.now()
            session.commit()
            
            return JSONResponse({ 'finished': True, 'winner': winner })
        
        model_plays = evaluate_game_state( game ) 
            
        if len( model_plays ) == 0:
            return JSONResponse({ 'finished': True, 'winner': None, 'draw': True })
        
        agent_row, agent_col = define_agent_play( game )
        
        create_play( session, game, player = 'O', row = agent_row, col = agent_col )

        if winner := verify_win( game ):
            
            game.finished = True
            game.finished_at = datetime.now()
            session.commit()

            return JSONResponse({ 'finished': True, 'winner': winner, 'row': agent_row, 'col': agent_col  })
            
        return JSONResponse({ 'finished': False, 'winner': None, 'row': agent_row, 'col': agent_col })

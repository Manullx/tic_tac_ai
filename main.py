
from datetime import datetime
from sqlmodel import Session, SQLModel, select
from sqlalchemy import func

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from db import engine, Game, Play
from rl.enviroment import estimate_reward
from rl.agent import define_agent_play


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


def winning_draw( current_game: Game ) -> str | None:

    last_play = current_game.plays[-1]
    
    row_formation = [ play.player for play in current_game.plays if play.row == last_play.row ]
    if len( row_formation ) == 3 and len( row_formation_set := set( row_formation ) ) == 1:

        return row_formation_set.pop()
    
    col_formation = [ play.player for play in current_game.plays if play.col == last_play.col ]
    if len( col_formation ) == 3 and len( col_formation_set := set( col_formation ) ) == 1:

        return col_formation_set.pop()
    
    if (last_play.row, last_play.col) in [(0, 0), (1, 1), (2, 2), (0, 2), (2, 0)]:

        first_diagonal_formation = [ play.player for play in current_game.plays if ( play.row, play.col ) in [(0, 0), (1, 1), (2, 2)] ]
        if len( first_diagonal_formation ) == 3 and len( first_diagonal_formation_set := set( first_diagonal_formation ) ) == 1:

            return first_diagonal_formation_set.pop()
        
        second_diagonal_formation = [ play.player for play in current_game.plays if ( play.row, play.col ) in [(0, 2), (1, 1), (2, 0)] ]
        if len( second_diagonal_formation ) == 3 and len( second_diagonal_formation_set := set( second_diagonal_formation ) ) == 1:

            return second_diagonal_formation_set.pop()
    
    if last_play.play_n == 8:

        return "|"
    
    return None
    

#FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)


#Routes
@app.get("/")
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
        
        player_play = Play( game_id = game.id, play_n = len( game.plays ), player = "X", row = player_row, col = player_col, reward = 0 )
        session.add( player_play )
        session.commit()
        session.refresh( game )
        
        if winner := winning_draw( game ):

            if winner == "|":

                game.draw = True
                game.finished = True
                game.finished_at = datetime.now()

                session.commit()

                return JSONResponse({ 'finished': True, 'winner': None, 'draw': True })

            game.winner = winner
            game.finished = True
            game.finished_at = datetime.now()

            last_agent_play = game.plays[-2]
            last_agent_play.reward = 0
            
            session.add( last_agent_play )

            session.commit()
            
            return JSONResponse({ 'finished': True, 'winner': winner })
        
        agent_row, agent_col = define_agent_play( session, game )
        agent_reward = estimate_reward( game, agent_row, agent_col )

        agent_play = Play( game_id = game.id, play_n = len( game.plays ), player = "O", row = agent_row, col = agent_col, reward = agent_reward )
        session.add( agent_play )
        session.commit()
        session.refresh( game )

        if winner := winning_draw( game ):

            game.winner = winner
            game.finished = True
            game.finished_at = datetime.now()

            last_agent_play = game.plays[-1]
            last_agent_play.reward = last_agent_play.reward + 1

            session.add( last_agent_play )

            session.commit()

            return JSONResponse({ 'finished': True, 'winner': winner, 'row': agent_row, 'col': agent_col  })
            
        return JSONResponse({ 'finished': False, 'winner': None, 'row': agent_row, 'col': agent_col })


#Dashboard
@app.get("/dashboard")
def get_quant_metrics():

    with Session(engine) as session:

        finished_total_games = session.exec( select( func.count(Game.id) ).where( Game.finished ) ).first()
        winning_total_games = session.exec( select( Game.winner, func.count(Game.id) ).where( Game.finished, Game.draw == False ).group_by( Game.winner ) ).fetchall()
        draw_total_games = session.exec( select( func.count(Game.id) ).where( Game.draw ) ).first()
        print(winning_total_games)
        return JSONResponse(
            {"totalFinished": finished_total_games, "winning_total": [ {"player": player, "player_total_winning": total } for player, total in winning_total_games], "totalDraw": draw_total_games}, 
            status_code = 200 
        )
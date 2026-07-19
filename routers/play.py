from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, Field

from sqlmodel import Session

from db import get_session
from models.play import Play, Players
from rules.game import check_winning
from services.game import get_game
from services.play import create_play

from rl.enviroment import estimate_play_reward
from rl.agent import define_agent_play


class PostPlayRequest(BaseModel):

    game_id: int
    row: int = Field( ge = 0, le = 2 )
    col: int = Field( ge = 0, le = 2 )


class PostPlayResponse(BaseModel):

    finished: bool = Field( default = False )
    winner: Players | None = Field( default = None )
    draw: bool = Field( default = False )
    player_play: Play
    agent_play: Play | None


play_router = APIRouter( prefix = "/play", tags = ["play"] )


@play_router.post("/", response_model = PostPlayResponse, status_code = status.HTTP_201_CREATED )
def post_play(*, session: Session = Depends(get_session), req: PostPlayRequest ):

    game = get_game( parent_session = session, game_id = req.game_id )
    
    if game.finished:

        raise HTTPException( detail = "Game is already finished.", status_code = status.HTTP_400_BAD_REQUEST )
    
    player_reward = estimate_play_reward( current_game = game, player = Players.x, row = req.row, col = req.col )
    player_play = create_play( parent_session = session, game_id = game.id, play_n = len(game.plays), player = Players.x, row = req.row, col = req.col, reward = player_reward )

    if winner := check_winning( game ):

        game.finished = True
        game.winner = winner
        game.finished_at = datetime.now()

        session.add(game)
        session.commit()
        
        return PostPlayResponse( finished = game.finished, winner = game.winner, player_play = player_play )
    
    session.refresh(game)

    if len(game.plays) == 9:

        game.finished = True
        game.draw = True
        game.finished_at = datetime.now()
        
        session.add(game)
        session.commit()

        return PostPlayResponse( finished = game.finished, draw = game.draw, player_play = player_play )
    
    agent_row, agent_col = define_agent_play( parent_session = session, current_game = game)
    agent_reward = estimate_play_reward( current_game = game, player = Players.o, row = agent_row, col = agent_col )
    agent_play = create_play( parent_session = session, game_id = game.id, play_n = len(game.plays), player = Players.o, row = agent_row, col = agent_col, reward = agent_reward )

    session.add(agent_play)
    session.commit()

    if winner := check_winning( game ):

        game.finished = True
        game.winner = winner
        game.finished_at = datetime.now()

        session.add(game)
        session.commit()

        return PostPlayResponse( finished = game.finished, winner = game.winner, player_play = player_play, agent_play = agent_play)

    
    return PostPlayResponse( player_play = player_play, agent_play = agent_play )
from fastapi import HTTPException

from sqlmodel import Session, select, col as column

from models.play import Play, Players
from services.game import get_game

from rl.enviroment import estimate_play_reward

def create_play( parent_session: Session, game_id: int, play_n: int, player: Players, row: int, col: int, reward: float ) -> Play:
    
    if parent_session.exec( select(Play).where( Play.game_id == game_id, Play.row == row, Play.col == col) ).first():

        raise HTTPException( detail = "The row and column for the move have already been selected.", status_code = 404 )

    new_play = Play( game_id = game_id, player = player, play_n = play_n, row = row, col = col )

    parent_session.add(new_play)
    parent_session.commit()
    parent_session.refresh(new_play)

    return new_play
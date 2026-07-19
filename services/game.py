from datetime import datetime

from fastapi import HTTPException, status

from sqlmodel import Session, select

from models.game import Game


def create_game( parent_session: Session ) -> Game:

    new_game = Game( started_at = datetime.now() )

    parent_session.add(new_game)
    parent_session.commit()
    parent_session.refresh(new_game)
    
    return new_game
    

def get_game( parent_session: Session, game_id: int ) -> Game:

    game = parent_session.exec(
        select(Game).where( Game.id == game_id )
    ).first()

    if game is None:
        
        raise HTTPException( detail = "Game not found", status_code = status.HTTP_404_NOT_FOUND)
    
    return game 
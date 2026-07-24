from typing import List
from sqlalchemy import func

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from db import get_session
from models.game import Game


class GetGameMetricsResponse(BaseModel):

    total_games: int
    finished_games: int
    drawed_games: int

    players_winnings: List[dict]


dashboard_router = APIRouter( prefix = "/dashboard", tags = ["dashboard"] )

@dashboard_router.get("/game")
def get_game_metrics( parent_session: Session = Depends(get_session)):

    total_games = parent_session.exec( select( func.count(Game.id) ) ).first()
    finished_games = parent_session.exec( select( func.count(Game.id) ).where( Game.finished ) ).first()
    drawed_games = parent_session.exec( select( func.count(Game.id) ).where( Game.finished, Game.draw ) ).first()
    
    players_winnings = parent_session.exec( select(Game.winner, func.count(Game.id) ).where( Game.finished, Game.draw == False ).group_by( Game.winner ) ).fetchall()
    
    return GetGameMetricsResponse(
        total_games = total_games,
        finished_games = finished_games,
        drawed_games = drawed_games,
        players_winnings = [ { 'player': player, "winnings": winnings} for player, winnings in players_winnings ]
    )
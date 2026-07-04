from sqlmodel import Session, select

from db import Game


def estimate_reward( current_game: Game, row: int, col: int ) -> None:

    reward = 0.1
    
    row_formation = [ p.player for p in current_game.plays if p.row == row]
    col_formation = [ p.player for p in current_game.plays if p.col == col ]
    first_diagonal = [ p.player for p in current_game.plays if ( p.row, p.col ) in [(0, 0), (1, 1), (2, 2)] ] if ( row, col ) in [(0, 0), (1, 1), (2, 2)] else None
    second_diagonal = [ p.player for p in current_game.plays if ( p.row, p.col ) in [(0, 2), (1, 1), (2, 0)] ] if ( row, col ) in [(0, 2), (1, 1), (2, 0)] else None

    #Prevent player from winning
    reward += len([ formation for formation in [ row_formation, col_formation, first_diagonal, second_diagonal ] if formation == ["X", "X"]]) * 0.15
    
    #Almost winning
    reward += len([ formation for formation in [ row_formation, col_formation, first_diagonal, second_diagonal ] if formation == ["O"]]) * 0.3

    return reward

from sqlmodel import Session, select

from models.game import Game
from models.play import Players

def estimate_play_reward( current_game: Game, player: Players, row: int, col: int ) -> None:
    
    reward = 0.1
    opponent = Players.o if player == Players.x else Players.x
    
    row_formation = [ p.player for p in current_game.plays if p.row == row]
    col_formation = [ p.player for p in current_game.plays if p.col == col ]
    first_diagonal = [ p.player for p in current_game.plays if ( p.row, p.col ) in [(0, 0), (1, 1), (2, 2)] ] if ( row, col ) in [(0, 0), (1, 1), (2, 2)] else None
    second_diagonal = [ p.player for p in current_game.plays if ( p.row, p.col ) in [(0, 2), (1, 1), (2, 0)] ] if ( row, col ) in [(0, 2), (1, 1), (2, 0)] else None

    #winning
    if ([ player ] * 3) in [row_formation, col_formation, first_diagonal, second_diagonal]:

        return 1
    
    #Prevent player from winning
    for formation in [ row_formation, col_formation, first_diagonal, second_diagonal]:
    
        if formation == ( [ opponent ] * 2) :
            
            reward += 0.2
    
    #Almost winning
    for formation in [ row_formation, col_formation, first_diagonal, second_diagonal]:
        
        if formation == ( [ player ] * 2 ):
            
            reward += 0.3

    return reward

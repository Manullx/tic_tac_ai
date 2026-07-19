
from models.game import Game
from models.play import Players

def check_winning( current_game: Game ) -> Players | None:

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
    
    return None
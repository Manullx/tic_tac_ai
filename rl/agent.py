import random
from typing import List
from sqlmodel import Session, select, col

from db import Game, Play


def evaluate_game_state( session: Session, current_game: Game ) -> List[ float ]:

    def select_equal_games( games_ids: set, play: Play ):

        query = select( Play ).where( col( Play.game_id ).in_( games_ids ), Play.play_n == play.play_n, Play.row == play.row, Play.col == play.col )
        result = [ play.game_id for play in session.exec( query ) ]

        return result[ : len(result) - 1]


    game_state = {
        '0_0': 0,
        '0_1': 0,
        '0_2': 0,
        '1_0': 0,
        '1_1': 0,
        '1_2': 0,
        '2_0': 0,
        '2_1': 0,
        '2_2': 0,
    }

    for play in current_game.plays:
        del game_state[f'{play.row}_{play.col}']

    current_play_n = len(current_game.plays)

    query = select( Play ).where( Play.play_n == 0, Play.row == current_game.plays[0].row, Play.col == current_game.plays[0].col )
    equal_games_ids = [ play.game_id for play in session.exec( query ) if play.game_id != current_game.id ]
    
    for play in current_game.plays[ 1 : ]:
        
        equal_games_ids = select_equal_games( equal_games_ids, play )
        
    for row_i in range(0, 3):

        for col_i in range(0, 3):
            
            if f'{row_i}_{col_i}' not in game_state.keys():

                continue

            query = select( Play ).where( col( Play.game_id ).in_(equal_games_ids), Play.play_n == current_play_n, Play.row == row_i, Play.col == col_i )
            
            square_rewards = []
            for play in session.exec( query ):

                query = select( Game ).where( Game.id == play.game_id )
                game = session.exec( query ).first()
                game_total_rewards = sum( [ p.reward for p in game.plays if p.play_n >= current_play_n and p.player == "O" ] )

                square_rewards.append(game_total_rewards)

            game_state[ f'{row_i}_{col_i}'] = sum( square_rewards ) / len( square_rewards ) if len( square_rewards ) >= 1 else 0

    return [( int(key.split("_")[0] ), int(key.split("_")[1]), value ) for key, value in game_state.items() ]


def define_agent_play( session: Session, current_game: Game ) -> tuple:

    evaluated_game = evaluate_game_state( session, current_game )
    print(f"Game ID: {current_game.id}\tPlay n: { len(current_game.plays) }\tEvaluated Game: { evaluated_game }")
    row, col, choice_mean = max(evaluated_game, key = lambda s: s[2])

    return (row, col)
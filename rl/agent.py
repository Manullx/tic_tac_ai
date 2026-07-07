import random
import numpy as np
from typing import List
from sqlmodel import Session, select, col

from db import Game, Play


def evaluate_game_state( session: Session, current_game: Game ) -> List[ float ]:

    def select_equal_games( games_ids: set, play: Play ):

        query = select( Play ).where( col( Play.game_id ).in_( games_ids ), Play.play_n == play.play_n, Play.row == play.row, Play.col == play.col )
        result = [ play.game_id for play in session.exec( query ) ]

        return result[ : len(result) - 1]


    current_play_n = len(current_game.plays)
    game_rewards = np.full( shape = (3, 3), fill_value = 0.2 if current_play_n == 1 else 0.1)

    query = select( Play ).where( Play.play_n == 0, Play.row == current_game.plays[0].row, Play.col == current_game.plays[0].col )
    equal_games_ids = [ play.game_id for play in session.exec( query ) if play.game_id != current_game.id ]
    
    for play in current_game.plays[ 1 : ]:
        
        equal_games_ids = select_equal_games( equal_games_ids, play )
        
    for row_i in range(0, 3):

        for col_i in range(0, 3):

            if ( row_i, col_i ) in [ ( current_game_play.row, current_game_play.col ) for current_game_play in current_game.plays ]:

                game_rewards[row_i][col_i] = 0
                continue

            query = select( Play ).where( col( Play.game_id ).in_(equal_games_ids), Play.play_n == current_play_n, Play.row == row_i, Play.col == col_i )
            
            square_rewards = []
            for play in session.exec( query ):

                query = select( Game ).where( Game.id == play.game_id )
                game = session.exec( query ).first()
                game_total_rewards = sum( [ p.reward for p in game.plays if p.play_n >= current_play_n and p.player == "O" ] )

                square_rewards.append(game_total_rewards)

            if square_rewards_len:= len(square_rewards) >= 1:

                game_rewards[row_i][col_i] = sum( square_rewards ) / square_rewards_len
    

    game_weights = game_rewards / game_rewards.sum()
    return game_weights.reshape(1, 9)[0]


def define_agent_play( session: Session, current_game: Game ) -> tuple:

    game_weights = evaluate_game_state( session, current_game )
    agent_choice = np.random.choice(9, size = 1, p = game_weights)[0]

    return [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][agent_choice]
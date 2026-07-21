import random
import numpy as np
from typing import List
from sqlalchemy import func
from sqlmodel import Session, select, col, or_, and_

from models.game import Game
from models.play import Play


def evaluate_game_state( session: Session, current_game: Game ) -> List[ float ]:    

    play_n = len(current_game.plays)
    selected_squares = [(p.row, p.col) for p in current_game.plays]
    game_rewards = np.zeros( shape = (3, 3) )
    
    equal_plays_q = select( Play.game_id, func.count(Play.game_id).label("total_plays") ).where(
        Play.game_id != current_game.id,
        or_(*[ and_(Play.play_n == current_p.play_n, Play.row == current_p.row, Play.col == current_p.col) for current_p in current_game.plays])
    ).group_by( Play.game_id )

    identical_games = [ game_id for game_id, identical_plays in session.exec(equal_plays_q) if identical_plays == play_n ]

    for row_i in range(0, 3):

        for col_i in range(0, 3):

            if (row_i, col_i) in selected_squares:

                continue
            
            square_rewards = []
            square_total_plays = 0
            for choice_p in session.exec( select(Play).where(col(Play.game_id).in_(identical_games), Play.play_n == play_n, Play.row == row_i, Play.col == col_i ) ):
                
                if not choice_p.game.finished:

                    continue
                
                if game_plays := [choice_game_p.reward for choice_game_p in choice_p.game.plays if choice_game_p.play_n >= play_n]:
                    
                    square_rewards.append( sum(game_plays) * len(game_plays) )
                    square_total_plays += len(game_plays)
                    
            if len(square_rewards):
                
                game_rewards[row_i][col_i] = sum(square_rewards) / square_total_plays
                continue

            else:

                game_rewards[row_i][col_i] = 0.1
    
    
    abs_min_actions_reward = np.abs( game_rewards.min() )
    
    if abs_min_actions_reward == 0:
        
        return game_rewards / game_rewards.sum()

    game_rewards = game_rewards + abs_min_actions_reward
    game_rewards[ game_rewards == 0 ] = 0.1
    game_rewards[ game_rewards == abs_min_actions_reward ] = 0

    return game_rewards / game_rewards.sum()


def define_agent_play( parent_session: Session, current_game: Game ) -> tuple:

    game_weights = evaluate_game_state( parent_session, current_game )
    agent_choice = np.random.choice(9, size = 1, p = game_weights.reshape(1, 9)[0])[0]
    
    return [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)][agent_choice]
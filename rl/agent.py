import random
from typing import List

from db import Game


def evaluate_game_state( game: Game ) -> List[ float ]:
    
    model_plays = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2)
    ]
    
    for play in game.plays:
        model_plays.remove( (play.row, play.col) )

    return model_plays


def define_agent_play( game: Game ) -> tuple:

    eval_game = evaluate_game_state( game )

    return random.choice( eval_game )
import random

from db import Game

from .enviroment import evaluate_game_state


def define_agent_play( game: Game ) -> tuple:

    eval_game = evaluate_game_state( game )

    return random.choice( eval_game )
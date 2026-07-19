from enum import Enum

from sqlmodel import SQLModel, Field, Relationship

from models.game import Game


class Players( str, Enum ):

    x = "X"
    o = "O"

class Play( SQLModel, table = True ):

    play_id: int | None = Field( default = None, primary_key = True )
    play_n: int
    player: Players
    row: int
    col: int
    reward: float = Field( default = 0 )

    game_id: int = Field( default = None, foreign_key = "game.id" )
    game: Game | None = Relationship( back_populates = "plays" )
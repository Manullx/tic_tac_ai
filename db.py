from typing import List
from datetime import datetime
from sqlmodel import Session, Column, JSON, Field, SQLModel, create_engine, Relationship


#Models
class Game( SQLModel, table = True ):

    id: int | None = Field( default = None, primary_key = True )
    finished: bool = Field( default = False )
    started_at:  datetime
    finished_at: datetime | None

    plays: list["Play"] | None = Relationship( back_populates = "game" )


class Play( SQLModel, table = True ):

    play_id: int | None = Field( default = None, primary_key = True )
    play_n: int
    player: str
    row: int
    col: int
    reward: float

    game_id: int = Field( default = None, foreign_key = "game.id" )
    game: Game | None = Relationship( back_populates = "plays" )


db_name = "db.sqlite"
db_uri = f"sqlite:///{db_name}"

engine = create_engine( db_uri, echo = False )

SQLModel.metadata.create_all( engine )

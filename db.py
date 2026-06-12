from typing import List
from datetime import datetime
from sqlmodel import Session, Column, JSON, Field, SQLModel, create_engine


#Models
class Game( SQLModel, table = True ):

    id: int | None = Field( default = None, primary_key = True )
    finished: bool = Field( default = False )
    started_at:  datetime
    finished_at: datetime | None


class Play( SQLModel, table = True ):

    game_id: int = Field( foreign_key = "game.id" )
    play_id: int | None = Field( default = None, primary_key = True )
    play_n: int
    player: str
    row: int
    col: int
    reward: float


db_name = "db.sqlite"
db_uri = f"sqlite:///{db_name}"

engine = create_engine( db_uri, echo = False )
session = Session( engine )

SQLModel.metadata.create_all( engine )
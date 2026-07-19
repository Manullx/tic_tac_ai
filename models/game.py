from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Game( SQLModel, table = True ):

    id: int | None = Field( default = None, primary_key = True )
    finished: bool = Field( default = False )
    winner: str | None = Field( default = None, max_length = 1 )
    draw: bool = Field( default = False )
    started_at:  datetime
    finished_at: datetime | None

    plays: list["Play"] | None = Relationship( back_populates = "game" )
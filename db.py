from sqlmodel import Session, SQLModel, create_engine

import models.game
import models.play

db_name = "db.sqlite"
db_uri = f"sqlite:///{db_name}"

engine = create_engine( db_uri, echo = False )

SQLModel.metadata.create_all( engine )

def get_session():

    with Session( engine ) as session:

        yield session
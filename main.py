from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.game import game_router
from routers.play import play_router
from routers.dashboard import dashboard_router
    

#FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router( game_router )
app.include_router( play_router )
app.include_router( dashboard_router )

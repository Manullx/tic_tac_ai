import random
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class GameState( BaseModel ):

    state: list


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)


# @app.get("/")
# def index():

#     return HTMLResponse( open("src/index.html").read(), status_code = 200, media_type = "text/html" )


@app.post("/square")
async def square( game_state: GameState ):
    
    req_body = game_state.model_dump()
    state = req_body['state']


    return JSONResponse({ 'row': random.randint( 1, 3 ), 'col': random.randint(1, 3) })
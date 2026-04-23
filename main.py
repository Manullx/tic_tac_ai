import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Square( BaseModel ):

    row: int
    col: int


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.post("/square")
async def square( sqr: Square ):
    
    return JSONResponse({ 'row': random.randint( 1, 3 ), 'col': random.randint(1, 3) })
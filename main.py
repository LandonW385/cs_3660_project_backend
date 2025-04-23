from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

import json

from controllers import login_controller, store_controller, spotify_controller, music_queue_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(login_controller.router)
app.include_router(store_controller.router)
app.include_router(spotify_controller.router)
app.include_router(music_queue_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TuneGether API"}


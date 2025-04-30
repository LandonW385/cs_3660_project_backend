from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

import json

from config import settings
from controllers import login_controller, store_controller, spotify_controller, music_queue_controller
from middleware.api_gateway_middleware import ApiGatewayMiddleware
from middleware.auth_middleware import AuthMiddleware

app = FastAPI(title="TuneGether Backend", version="1.0.0")

app.add_middleware(AuthMiddleware)

if settings.app_env == "local":
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["http://localhost:5173"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
    )

app.add_middleware(ApiGatewayMiddleware)


app.include_router(login_controller.router)
app.include_router(store_controller.router)
app.include_router(spotify_controller.router)
app.include_router(music_queue_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the TuneGether API"}

@app.get("/health")
def read_root():
    return {"message": "ok"}
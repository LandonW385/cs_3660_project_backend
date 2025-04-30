from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str
    allow_origins: list[AnyHttpUrl] 
    api_gateway_token: str
    secret_key: str
    algorithm: str
    client_id: str
    client_secret: str


    class Config:
        env_file = ".env"


settings = Settings()
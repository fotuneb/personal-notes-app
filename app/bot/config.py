# app/bot/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    api_url: str

    class Config:
        env_file = ".env"

settings = Settings()

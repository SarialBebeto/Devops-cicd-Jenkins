import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(
        default='sqlite:///./test.db', 
        env='DATABASE_URL'
    )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()

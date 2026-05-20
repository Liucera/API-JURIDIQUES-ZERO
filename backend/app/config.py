import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://admin:Juridiques2026@db:5432/juridiques_zero")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://ollama:11434")

settings = Settings()

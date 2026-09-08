"""Application configuration"""

from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./seedforge.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Data paths
    DATA_DIR: str = "./data"
    SEEDS_DIR: str = "./data/seeds"
    OUTPUT_DIR: str = "./output"
    
    # Performance
    MAX_WORKERS: int = 4
    BATCH_SIZE: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

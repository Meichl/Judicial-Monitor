from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/judicial_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Judicial Monitor API"
    
    # Scraping
    SCRAPER_CONCURRENCY: int = 5
    SCRAPER_TIMEOUT: int = 30
    
    # Cache
    CACHE_TTL: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
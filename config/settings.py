from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Google Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Tavily
    TAVILY_API_KEY: str
    
    # Application
    APP_NAME: str = "AI Research Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Storage
    CHROMA_DB_PATH: str = "./data/chroma_db"
    REPORTS_PATH: str = "./reports"
    
    # API Settings
    MAX_RESEARCH_DEPTH: int = 5
    MAX_SEARCH_RESULTS: int = 10
    SEARCH_TIMEOUT: int = 30
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


settings = Settings()

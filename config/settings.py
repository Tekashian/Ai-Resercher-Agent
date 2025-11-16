from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
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

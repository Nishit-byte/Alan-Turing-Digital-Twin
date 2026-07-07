from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    gemini_api_key: str
    chroma_db_path: str = "./chroma_db"
    data_raw_path: str = "./data/raw"
    data_processed_path: str = "./data/processed"
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
Path(settings.data_raw_path).mkdir(parents=True, exist_ok=True)
Path(settings.data_processed_path).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_db_path).mkdir(parents=True, exist_ok=True)
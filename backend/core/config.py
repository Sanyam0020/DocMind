from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DocuMind"
    app_version: str = "0.1.0"

    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
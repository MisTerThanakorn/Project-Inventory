from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("backend/.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/project_inventory"
    jwt_secret: str = "change-me"
    jwt_expires_in_minutes: int = 60 * 24 * 7
    app_name: str = "Project Inventory API"
    app_host: str = "0.0.0.0"
    app_port: int = 4000
    client_origin: str = "http://localhost:3000"


@lru_cache
def get_settings() -> Settings:
    return Settings()

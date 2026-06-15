from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_user: str = "fundfinance"
    postgres_password: str = "fundfinance"
    postgres_db: str = "fundfinance"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url: str = (
        "postgresql+psycopg://fundfinance:fundfinance@localhost:5432/fundfinance"
    )

    app_env: str = "local"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

"""Application configuration utilities."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Dictionary Agent API"
    description: str = "Context-aware dictionary service with ML-powered sense disambiguation"
    version: str = "1.0.0"

    cors_allow_origins: list[str] = ["*"]

    redis_host: str = "localhost"
    redis_port: int = 6379
    cache_ttl: int = 86_400

    free_dictionary_url: str = "https://api.dictionaryapi.dev/api/v2/entries/en/"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

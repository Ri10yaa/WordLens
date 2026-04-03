"""Configuration helpers for the dictionary agent."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    backend_url: str = "http://localhost:8000"
    hf_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache
def get_settings() -> AgentSettings:
    return AgentSettings()


settings = get_settings()

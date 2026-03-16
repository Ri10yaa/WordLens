"""Configuration helpers for the LLM agent."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str
    backend_url: str = "http://localhost:8000"
    planner_model: str = "gpt-4o-mini"
    response_model: str = "gpt-4"


@lru_cache
def get_settings() -> AgentSettings:
    return AgentSettings()


settings = get_settings()

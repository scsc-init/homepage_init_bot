from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    rabbitmq_host: str
    token: str
    command_prefix: str

    model_config = SettingsConfigDict(env_file=".env", frozen=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore

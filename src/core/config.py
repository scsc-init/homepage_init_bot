from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    rabbitmq_host: str = "rabbitmq"
    main_backend_host: str = "backend"
    discord_receive_queue: str = "discord_bot_queue"
    token: str
    command_prefix: str = "!"
    api_secret: str

    model_config = SettingsConfigDict(env_file=".env", frozen=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore

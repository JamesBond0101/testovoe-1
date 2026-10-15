from functools import lru_cache

from pydantic import AnyHttpUrl, PositiveInt, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )

    app_name: str = "Deribit Price Service"
    database_url: PostgresDsn
    celery_broker_url: RedisDsn
    deribit_base_url: AnyHttpUrl = AnyHttpUrl("https://www.deribit.com/api/v2/public/get_index_price")
    collection_interval_seconds: PositiveInt = 60


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str 
    app_env: Literal["development", "test", "production"] = "production"

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db"

    secret_key: str 
    algorithm: Literal['HS256'] = 'HS256'
    access_token_expire_minutes: int
    refresh_token_expire_days: int = 7 # просто 7 нельзя писать,а то это аннотация типа будет

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        # Кавычки откладывают вычисление типа
        if self.app_env == "production" and len(self.secret_key) < 32:
            raise ValueError("secret_key must be at least 32 characters in production")
        return self


@lru_cache 
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

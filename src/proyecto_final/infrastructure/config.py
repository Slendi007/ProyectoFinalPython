from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Proyecto Final - Orders API"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "sqlite:///./orders.db"

    jwt_secret_key: SecretStr | None = None
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()

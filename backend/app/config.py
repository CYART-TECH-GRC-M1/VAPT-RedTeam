from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CyGRC VAPT & Red Team API"
    app_version: str = "0.1.0"

    database_url: str = (
        "postgresql+asyncpg://cygrc:cygrc@localhost:5432/cygrc"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
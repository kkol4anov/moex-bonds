from functools import lru_cache
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    database_url: str

    iss_base_url: str = "https://iss.moex.com/iss"
    log_level: str = "INFO"
    db_ssl: bool = False

    @computed_field
    @property
    def async_database_url(self) -> str:
        # Render gives postgresql:// while asyncpg-engine needs postgresql+asyncpg://
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

@lru_cache
def get_settings() -> Settings:
    return Settings() #type: ignore[call-arg]
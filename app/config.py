from pathlib import Path
from typing import Literal

from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: Literal["dev", "prod"] = "dev"
    PROJECT_NAME: str | None = "Wooki Waitlist"
    API_PREFIX: str | None = "/api/v1"
    X_API_KEY: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: str | None = None
    POSTGRES_DB: str | None = None

    @model_validator(mode="after")
    def apply_environment_defaults(self):
        if self.ENVIRONMENT == "dev":
            self.X_API_KEY = self.X_API_KEY or "dev-api-key"
            self.POSTGRES_USER = self.POSTGRES_USER or "test_user"
            self.POSTGRES_PASSWORD = self.POSTGRES_PASSWORD or "test_pass"
            self.POSTGRES_HOST = self.POSTGRES_HOST or "localhost"
            self.POSTGRES_PORT = self.POSTGRES_PORT or "5432"
            self.POSTGRES_DB = self.POSTGRES_DB or "test_db"
            return self

        required_fields = {
            "X_API_KEY": self.X_API_KEY,
            "POSTGRES_USER": self.POSTGRES_USER,
            "POSTGRES_PASSWORD": self.POSTGRES_PASSWORD,
            "POSTGRES_HOST": self.POSTGRES_HOST,
            "POSTGRES_PORT": self.POSTGRES_PORT,
            "POSTGRES_DB": self.POSTGRES_DB,
        }

        missing_fields = [name for name, value in required_fields.items() if not value]
        if missing_fields:
            missing_as_text = ", ".join(missing_fields)
            raise ValueError(f"Missing required settings for ENVIRONMENT=prod: {missing_as_text}")

        return self

    model_config = ConfigDict(
        extra="allow",
        env_file=(
            Path(__file__).resolve().parents[1] / ".env",
            Path(__file__).resolve().parents[2] / ".env",
        ),
        env_file_encoding="utf-8",   
    )

settings = Settings()
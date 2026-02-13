"""
Application configuration using Pydantic BaseSettings.

Loads configuration from environment variables with validation.
"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are loaded from .env file or environment variables.
    """

    # Database
    DATABASE_URL: str

    # Security
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: Literal["development", "production", "test"] = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

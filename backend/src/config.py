"""Configuration management for the Todo backend application."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    This class uses pydantic-settings to automatically load configuration
    from environment variables with the TODO_ prefix.
    """

    # Database configuration
    database_url: str
    """PostgreSQL database connection URL for Neon Serverless"""

    # Authentication configuration
    better_auth_secret: str
    """Secret key for JWT token signing and verification"""

    better_auth_algorithm: str = "HS256"
    """Algorithm used for JWT signing (default: HS256)"""

    # Server configuration
    host: str = "0.0.0.0"
    """Host address for the FastAPI server"""

    port: int = 8000
    """Port number for the FastAPI server"""

    debug: bool = False
    """Debug mode flag"""

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Uses LRU cache to ensure settings are loaded only once and reused
    throughout the application lifecycle.

    Returns:
        Settings: Configuration instance loaded from environment
    """
    return Settings()


# Export for convenience
settings = get_settings()

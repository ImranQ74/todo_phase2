"""Database dependency for FastAPI."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db


# Re-export get_db for convenience
__all__ = ["get_db"]

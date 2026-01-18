"""Dependency injection modules for FastAPI."""

from .auth import get_current_user_id, verify_task_ownership
from .database import get_db

__all__ = ["get_current_user_id", "verify_task_ownership", "get_db"]

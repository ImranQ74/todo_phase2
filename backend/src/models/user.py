"""User model for authentication reference."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Minimal user entity for reference.

    Note: Primary authentication is handled by Better Auth frontend.
    This model exists for database relationships and reference.

    Attributes:
        id: Primary key
        uuid: Unique user identifier
        email: User email address
        hashed_password: Password hash (not used directly in this implementation)
        created_at: Account creation timestamp
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: Optional[str] = Field(default=None, unique=True, index=True)
    email: str = Field(unique=True, max_length=255)
    hashed_password: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)

"""Task model representing a todo item owned by a user."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task entity representing a todo item.

    Each task belongs to a specific user and includes metadata for tracking
    creation and modification times.

    Attributes:
        id: Primary key (auto-incrementing integer)
        uuid: Unique identifier (UUID4 string)
        title: Task title (required, max 255 characters)
        description: Optional task description
        completed: Completion status (default: False)
        user_id: Foreign key referencing the user who owns this task
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()), unique=True, index=True)
    title: str = Field(max_length=255, description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    completed: bool = Field(default=False, description="Completion status")
    user_id: str = Field(index=True, description="User ID from JWT")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)

    def __repr__(self) -> str:
        """String representation of the Task object."""
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"

"""
Data models for the Todo application.

This module defines the Task dataclass used to represent individual todo items.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique auto-incrementing integer identifier
        title: Task title (required, non-empty string)
        description: Optional detailed description of the task
        completed: Boolean flag indicating completion status (default: False)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the task.

        Returns:
            Formatted string showing completion status, ID, and title
        """
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}. {self.title}"

    def display(self) -> str:
        """
        Return a detailed display string including description.

        Returns:
            Multi-line formatted string with all task details
        """
        status = "[x]" if self.completed else "[ ]"
        lines = [
            f"{status} Task #{self.id}",
            f"Title: {self.title}",
        ]
        if self.description:
            lines.append(f"Description: {self.description}")
        lines.append(f"Status: {'Completed' if self.completed else 'Incomplete'}")
        return "\n".join(lines)

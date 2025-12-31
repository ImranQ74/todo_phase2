"""
Todo task manager for in-memory CRUD operations.

This module provides the TodoManager class that handles all task management
operations including creating, reading, updating, deleting, and toggling
completion status of tasks.
"""

from typing import Optional

from .models import Task


class TaskNotFoundError(Exception):
    """Exception raised when a task with the specified ID is not found."""

    pass


class TodoManager:
    """
    Manages a collection of todo tasks in memory.

    This class maintains an in-memory list of Task objects and provides
    methods for CRUD operations plus completion toggling.
    """

    def __init__(self) -> None:
        """Initialize the TodoManager with an empty task list."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the todo list.

        Args:
            title: Task title (required, non-empty string)
            description: Optional detailed description (default: empty string)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip(),
            completed=False,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        """
        Get all tasks in the todo list.

        Returns:
            List of all Task objects ordered by ID (creation order)
        """
        return self._tasks.copy()

    def _find_task_by_id(self, task_id: int) -> Task:
        """
        Find a task by its ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The Task object with the specified ID

        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found")

    def update_task(
        self,
        task_id: int,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Task:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: The unique identifier of the task to update
            new_title: New title for the task (None to keep existing)
            new_description: New description (None to keep existing)

        Returns:
            The updated Task object

        Raises:
            TaskNotFoundError: If no task with the given ID exists
            ValueError: If new_title is provided but empty
        """
        task = self._find_task_by_id(task_id)

        if new_title is not None:
            if not new_title or not new_title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = new_title.strip()

        if new_description is not None:
            task.description = new_description.strip()

        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task from the todo list.

        Args:
            task_id: The unique identifier of the task to delete

        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self._find_task_by_id(task_id)
        self._tasks.remove(task)

    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The unique identifier of the task to toggle

        Returns:
            The updated Task object with toggled completion status

        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self._find_task_by_id(task_id)
        task.completed = not task.completed
        return task

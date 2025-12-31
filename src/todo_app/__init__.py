"""
Todo App - In-Memory Console Todo Application

A simple command-line todo application built following spec-driven
development principles. Phase I implements core CRUD + completion
operations with in-memory storage.
"""

from .cli import CLI
from .manager import TaskNotFoundError, TodoManager
from .models import Task

__version__ = "0.1.0"

__all__ = ["CLI", "Task", "TodoManager", "TaskNotFoundError"]

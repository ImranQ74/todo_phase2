"""
Command-line interface for the Todo application.

This module provides the CLI class that handles user interaction,
command parsing, and display formatting for the todo app.
"""

from typing import Optional

from .manager import TaskNotFoundError, TodoManager


class CLI:
    """
    Command-line interface for interacting with the TodoManager.

    Provides a command-based interface with input validation and
    user-friendly error messages.
    """

    def __init__(self) -> None:
        """Initialize the CLI with a new TodoManager instance."""
        self.manager = TodoManager()
        self.running = True

    def run(self) -> None:
        """
        Start the main CLI loop.

        Displays welcome message and processes user commands until
        the user chooses to exit.
        """
        self._print_welcome()
        while self.running:
            try:
                command = input("\n> ").strip()
                if command:
                    self._process_command(command)
            except KeyboardInterrupt:
                print("\n")
                self._handle_exit()
            except EOFError:
                print("\n")
                self._handle_exit()

    def _print_welcome(self) -> None:
        """Display welcome message and command help."""
        print("=" * 50)
        print("Welcome to Todo App - Phase I")
        print("=" * 50)
        print("\nAvailable commands:")
        print("  add <title> [description]  - Add a new task")
        print("  list                       - Show all tasks")
        print("  update <id>                - Update a task")
        print("  delete <id>                - Delete a task")
        print("  complete <id>              - Toggle task completion")
        print("  help                       - Show this help message")
        print("  quit / exit                - Exit the application")
        print()

    def _print_help(self) -> None:
        """Display command help."""
        print("\nAvailable commands:")
        print("  add <title> [description]  - Add a new task")
        print("  list                       - Show all tasks")
        print("  update <id>                - Update a task")
        print("  delete <id>                - Delete a task")
        print("  complete <id>              - Toggle task completion")
        print("  help                       - Show this help message")
        print("  quit / exit                - Exit the application")

    def _process_command(self, command: str) -> None:
        """
        Parse and execute a user command.

        Args:
            command: Raw command string from user input
        """
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()

        if cmd in ("quit", "exit"):
            self._handle_exit()
        elif cmd == "help":
            self._print_help()
        elif cmd == "add":
            self._handle_add(parts[1] if len(parts) > 1 else "")
        elif cmd == "list":
            self._handle_list()
        elif cmd == "update":
            self._handle_update(parts[1] if len(parts) > 1 else "")
        elif cmd == "delete":
            self._handle_delete(parts[1] if len(parts) > 1 else "")
        elif cmd == "complete":
            self._handle_complete(parts[1] if len(parts) > 1 else "")
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")

    def _handle_add(self, args: str) -> None:
        """
        Handle the 'add' command to create a new task.

        Args:
            args: Command arguments containing title and optional description
        """
        if not args:
            print("Error: Task title is required.")
            print("Usage: add <title> [description]")
            return

        # Split into title and description
        # Everything after first word can be description
        parts = args.split(maxsplit=1)
        title = parts[0]
        description = parts[1] if len(parts) > 1 else ""

        try:
            task = self.manager.add_task(title, description)
            print(f"\n✓ Task added successfully!")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            if task.description:
                print(f"  Description: {task.description}")
        except ValueError as e:
            print(f"Error: {e}")

    def _handle_list(self) -> None:
        """Handle the 'list' command to display all tasks."""
        tasks = self.manager.list_tasks()

        if not tasks:
            print("\nNo tasks found. Add a task with 'add <title>'.")
            return

        print(f"\n{'=' * 50}")
        print(f"{'ID':<5} {'Status':<8} {'Title':<30} {'Description'}")
        print(f"{'=' * 50}")

        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            # Truncate description to 30 chars if too long
            desc = task.description[:27] + "..." if len(task.description) > 30 else task.description
            print(f"{task.id:<5} {status:<8} {task.title[:30]:<30} {desc}")

        print(f"{'=' * 50}")
        print(f"Total: {len(tasks)} task(s)")

    def _handle_update(self, args: str) -> None:
        """
        Handle the 'update' command to modify an existing task.

        Args:
            args: Command arguments containing task ID
        """
        if not args:
            print("Error: Task ID is required.")
            print("Usage: update <id>")
            return

        try:
            task_id = int(args)
        except ValueError:
            print(f"Error: Invalid task ID '{args}'. Please provide a number.")
            return

        try:
            # Find the task first to show current values
            task = self.manager._find_task_by_id(task_id)
            print(f"\nUpdating Task #{task_id}")
            print(f"Current title: {task.title}")
            print(f"Current description: {task.description}")

            # Prompt for new values
            print("\nEnter new values (press Enter to keep current value):")
            new_title = input(f"Title [{task.title}]: ").strip()
            new_description = input(f"Description [{task.description}]: ").strip()

            # Only update if user provided new values
            title_to_update = new_title if new_title else None
            desc_to_update = new_description if new_description else None

            if title_to_update is None and desc_to_update is None:
                print("\nNo changes made.")
                return

            self.manager.update_task(task_id, title_to_update, desc_to_update)
            print(f"\n✓ Task #{task_id} updated successfully!")

        except TaskNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    def _handle_delete(self, args: str) -> None:
        """
        Handle the 'delete' command to remove a task.

        Args:
            args: Command arguments containing task ID
        """
        if not args:
            print("Error: Task ID is required.")
            print("Usage: delete <id>")
            return

        try:
            task_id = int(args)
        except ValueError:
            print(f"Error: Invalid task ID '{args}'. Please provide a number.")
            return

        try:
            # Show task before deletion
            task = self.manager._find_task_by_id(task_id)
            confirm = input(f"\nDelete task '{task.title}'? (y/n): ").strip().lower()

            if confirm in ("y", "yes"):
                self.manager.delete_task(task_id)
                print(f"\n✓ Task #{task_id} deleted successfully!")
            else:
                print("\nDeletion cancelled.")

        except TaskNotFoundError as e:
            print(f"Error: {e}")

    def _handle_complete(self, args: str) -> None:
        """
        Handle the 'complete' command to toggle task completion status.

        Args:
            args: Command arguments containing task ID
        """
        if not args:
            print("Error: Task ID is required.")
            print("Usage: complete <id>")
            return

        try:
            task_id = int(args)
        except ValueError:
            print(f"Error: Invalid task ID '{args}'. Please provide a number.")
            return

        try:
            task = self.manager.toggle_complete(task_id)
            status = "completed" if task.completed else "incomplete"
            print(f"\n✓ Task #{task_id} marked as {status}!")

        except TaskNotFoundError as e:
            print(f"Error: {e}")

    def _handle_exit(self) -> None:
        """Handle application exit."""
        print("\nThank you for using Todo App!")
        print("Note: All tasks are stored in memory and will be lost on exit.")
        self.running = False

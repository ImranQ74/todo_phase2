"""
Main entry point for the Todo application.

This script initializes and runs the command-line interface for the
in-memory todo task manager.
"""

from src.todo_app.cli import CLI


def main() -> None:
    """
    Start the Todo application.

    Creates a CLI instance and runs the main application loop.
    """
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()

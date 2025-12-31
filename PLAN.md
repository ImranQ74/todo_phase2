# Implementation Plan

## Version
0001 - Plan for Initial Specification

## Architecture Overview
- Single-file or small module structure under /src/todo_app/.
- Core: A TodoManager class handling in-memory storage (list of Task objects).
- Task: Dataclass with id, title, description, completed.
- CLI: Separate module or main script with loop parsing commands.
- Entry point: Console script via main loop.

## Project Structure
```
todo-app/
├── CONSTITUTION.md
├── SPECIFICATION.md
├── PLAN.md
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models.py       # Task dataclass
│       ├── manager.py      # TodoManager class
│       └── cli.py          # Command parsing & UI loop
├── main.py                 # Entry point
├── pyproject.toml          # UV config
├── README.md
└── .python-version
```

## Task Breakdown

### 1. Setup Project Skeleton
- ✓ UV venv and proper /src structure (already complete)

### 2. Define Task Dataclass
- File: `src/todo_app/models.py`
- Fields: id (int), title (str), description (str), completed (bool)
- Use `@dataclass` from stdlib

### 3. Implement TodoManager
- File: `src/todo_app/manager.py`
- Storage: List of Task objects
- Methods:
  - `add_task(title: str, description: str = "") -> Task`
  - `list_tasks() -> list[Task]`
  - `update_task(task_id: int, new_title: str | None = None, new_desc: str | None = None) -> Task`
  - `delete_task(task_id: int) -> None`
  - `toggle_complete(task_id: int) -> Task`
  - `_find_task_by_id(task_id: int) -> Task` (internal helper with error handling)
- Auto-incrementing ID counter

### 4. Implement CLI Loop
- File: `src/todo_app/cli.py`
- Command parser (split input into command + args)
- Commands: add, list, update, delete, complete, quit/exit
- User-friendly prompts and status messages
- Input validation and error handling

### 5. Add Main Entry Point
- File: `main.py`
- Imports CLI and runs the main loop
- Can be invoked directly: `python main.py`

### 6. Polish & UX
- Clear status indicators: [x] / [ ]
- Confirmation messages for all operations
- Helpful error messages
- Clean display formatting

## Technical Decisions
- **Data Model**: Use `@dataclass` from stdlib for Task
- **ID Generation**: Auto-incrementing counter starting at 1
- **Storage**: Simple list of Task objects (in-memory only)
- **CLI Style**: Command-based (e.g., "add", "list", "update 1")
- **Error Handling**: Raise custom exceptions, catch in CLI layer
- **Type Hints**: Full type annotations using `typing` module
- **Code Style**: PEP 8 compliant, documented with docstrings

## Implementation Order
1. models.py (Task dataclass)
2. manager.py (TodoManager class)
3. cli.py (CLI interface)
4. main.py (Entry point)
5. Testing & polish

## Validation Checklist
- [ ] All code follows PEP 8
- [ ] Type hints on all functions
- [ ] Docstrings on all classes and public methods
- [ ] Error handling for invalid inputs
- [ ] Confirmation messages for all operations
- [ ] Clean separation of concerns (models/manager/cli)

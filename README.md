# Todo App - Phase I

An in-memory Python console-based todo application built following spec-driven development principles.

## Project Status
- Phase: I (The Evolution of Todo)
- Status: Specification Approved (v0001)
- Next: Implementation Planning

## Technology Stack
- Python 3.13+
- UV for project management
- Standard library only (no external dependencies)

## Project Structure
```
todo-app/
├── src/
│   └── todo_app/
│       └── __init__.py
├── CONSTITUTION.md
├── SPECIFICATION.md
├── README.md
├── pyproject.toml
└── .python-version
```

## Development Principles
This project follows strict **spec-driven development**:
1. No code without approved specifications
2. AI-native workflow using Claude Code
3. Clean code with type hints and proper documentation
4. In-memory storage only (Phase I)
5. Console UI only

See `CONSTITUTION.md` for complete project principles and standards.

## Getting Started

### Prerequisites
- Python 3.13 or higher
- UV package manager

### Installation
```bash
# Create virtual environment with UV
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
source .venv/bin/activate
```

## Features (v0001)
See `SPECIFICATION.md` for complete feature details:
1. Add Task (title + optional description)
2. View Task List (all tasks with status)
3. Update Task (edit title/description)
4. Delete Task (remove by ID)
5. Mark as Complete (toggle completion status)

## Next Steps
1. ~~Create feature specifications~~ ✓ Complete
2. Design implementation plan
3. Build core todo functionality
4. Add tests

## License
TBD

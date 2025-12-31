# Project Constitution

## Project Name
Todo In-Memory Python Console App (Phase I: The Evolution of Todo)

## Core Principles
- **Spec-Driven Development**: All development must be guided by explicit, versioned specifications created using Spec-Kit Plus workflows.
- **AI-Native Workflow**: Use Claude Code (or compatible AI agent) for generation, refinement, and implementation based on specs and plans.
- **Clean Code & Best Practices**: Follow PEP 8 style guidelines, type hints (using typing module), meaningful naming, modular design, and separation of concerns.
- **Simplicity First**: No external dependencies beyond the Python standard library for this phase (in-memory only).
- **Testability**: Design code to be easily testable; include unit tests where appropriate in future iterations.
- **Reproducibility**: Use UV for project management, virtual environments, and dependency handling (even if no extras yet).

## Technology Constraints
- Python version: 3.13+
- Project management: UV (for venv, scripts, and future dependencies)
- Storage: In-memory only (e.g., list of dicts or dataclass instances); no files, databases, or persistence.
- UI: Command-line interface (console-based) only.
- No frameworks or external libraries.

## Quality & Engineering Standards
- All code must be readable, documented with docstrings, and structured in a proper Python package (/src layout).
- Tasks must have unique IDs, title, description, and completion status.
- Error handling: Graceful handling of invalid inputs (e.g., non-existent task IDs).
- Version control: All changes committed to Git with meaningful messages.

## Non-Negotiable Rules
- Do not write code without an approved specification and plan.
- Specifications evolve iteratively but must remain the source of truth.
- Prioritize user experience in CLI: clear prompts, feedback messages, and status indicators.

This constitution applies to all phases but is scoped to Phase I for this deliverable.

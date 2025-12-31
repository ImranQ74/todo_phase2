# Specification: In-Memory Console Todo App

## Version
0001 - Initial Core Specification

## Overview
Build a simple command-line Todo application that manages tasks entirely in memory. The app supports the 5 basic CRUD + completion operations. Tasks are stored in a global in-memory list and lost on exit.

## User Stories & Features

### 1. Add Task
- As a user, I can add a new task with a title and optional description.
- Acceptance Criteria:
  - Task receives a unique auto-incrementing integer ID.
  - Title is required (non-empty string).
  - Description is optional (default empty string).
  - Completion status defaults to incomplete (False).
  - Confirmation message shown with new task details.

### 2. View Task List
- As a user, I can list all tasks.
- Acceptance Criteria:
  - Displays task ID, title, completion status (e.g., [x] or [ ]), and truncated description.
  - Shows "No tasks" if empty.
  - Ordered by creation (oldest first) or ID.

### 3. Update Task
- As a user, I can update an existing task's title and/or description by ID.
- Acceptance Criteria:
  - Prompt for new title and/or description.
  - Preserve existing values if user skips.
  - Error if ID not found.
  - Confirmation of update.

### 4. Delete Task
- As a user, I can delete a task by ID.
- Acceptance Criteria:
  - Remove task from list.
  - Error if ID not found.
  - Confirmation message.

### 5. Mark as Complete
- As a user, I can toggle a task's completion status by ID.
- Acceptance Criteria:
  - Toggle between complete/incomplete.
  - Error if ID not found.
  - Updated status reflected in next list view.

## Non-Functional Requirements
- CLI loop: Menu-driven or command-based (e.g., commands like "add", "list", "update <id>", etc.).
- Input validation: Handle invalid commands/inputs gracefully.
- Exit command: "quit" or "exit" to end program.

## Out of Scope (Phase I)
- Persistence (files/DB)
- Due dates, priorities, categories
- GUI or web interface
- User authentication

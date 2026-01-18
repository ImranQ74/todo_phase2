# Project Constitution

## Project Name
Todo Full-Stack Web Application (Phase II: The Evolution of Todo)

## Core Principles
- **Spec-Driven Development**: All development must be guided by explicit, versioned specifications created using Spec-Kit Plus workflows.
- **AI-Native Workflow**: Use Claude Code (or compatible AI agent) for generation, refinement, and implementation based on specs and plans.
- **Clean Code & Best Practices**: Follow industry standards for each technology (PEP 8 for Python, React/Next.js best practices for frontend); type hints, meaningful naming, modular design, and separation of concerns.
- **Security-First**: Implement proper authentication, authorization, and user isolation at every layer.
- **Testability**: Design code to be easily testable; include unit tests and integration tests where appropriate.
- **Reproducibility**: Use UV for Python project management; consistent dependency handling across all components.

## Technology Constraints

### Frontend
- Framework: Next.js 16+ (using App Router)
- Language: TypeScript
- Authentication: Better Auth with JWT plugin
- Styling: Tailwind CSS (or similar modern styling solution)
- Must be responsive and accessible

### Backend
- Framework: Python FastAPI
- Python version: 3.13+
- ORM: SQLModel (for database interactions)
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)

### Infrastructure & DevOps
- Monorepo structure with separate frontend and backend directories
- Environment variables for all secrets (BETTER_AUTH_SECRET, DATABASE_URL, etc.)
- UV for Python dependency management

## API Specification

### Base URL
`/api/{user_id}/`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for a user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle task completion |

### Authentication
- All endpoints require a valid JWT token in the `Authorization: Bearer <token>` header
- Unauthorized requests must return 401 status code
- JWT verification uses the BETTER_AUTH_SECRET environment variable

### User Isolation
- All task operations must be filtered by `user_id`
- Users can only access, modify, or delete their own tasks
- Backend must enforce ownership verification on every request

## Data Model

### Task Entity
| Field | Type | Description |
|-------|------|-------------|
| id | UUID/Integer | Unique task identifier |
| title | String | Task title (required) |
| description | String | Task description (optional) |
| completed | Boolean | Completion status, default false |
| user_id | UUID/Integer | Foreign key to user owner |

## Quality & Engineering Standards
- All code must be readable, documented with docstrings (Python) and comments (TypeScript), and properly structured.
- RESTful principles: proper HTTP methods, status codes, and error responses.
- Error handling: Graceful handling of invalid inputs, proper HTTP error codes (400, 401, 404, 500).
- Version control: All changes committed to Git with meaningful messages following conventional commits.
- API documentation: OpenAPI/Swagger documentation for backend endpoints.

## Non-Negotiable Rules
- Do not write code without an approved specification and plan.
- Specifications evolve iteratively but must remain the source of truth.
- Never expose user data to unauthorized users; enforce user isolation at the database query level.
- Store secrets in environment variables, never in source code.
- All API endpoints require authentication; no public endpoints for user data.

## Spec-Kit Plus Organization
- `specs/phase1/` - Original console app specifications
- `specs/phase2/` - Full-stack web application specifications
- Each phase has its own subdirectory with versioned specs

This constitution applies to all phases. Phase II builds upon Phase I's foundation, evolving from a console app to a full-stack web application while maintaining Spec-Driven Development principles.

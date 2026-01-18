# Phase 2 Implementation Plan
## The Evolution of Todo: Full-Stack Web Application

## Executive Summary

This document outlines a step-by-step plan to execute Phase 2 of the "Evolution of Todo" project using Claude Code and spec-driven development. Phase 2 transforms the Phase 1 in-memory Python console app into a full-stack, multi-user web application with persistent storage, JWT authentication, and responsive UI.

**Core Constraint**: All code must be generated via Claude Code by refining specifications until correct output is achieved. No manual coding permitted.

**Project Timeline**: 6-12 hours over 1-2 days (assuming minimal refinement cycles)

**Final Deadline**: January 18, 2026

---

## Prerequisites

### Environment Setup
1. **Neon Serverless PostgreSQL**
   - Sign up at [neon.tech](https://neon.tech)
   - Create a new project
   - Copy the `DATABASE_URL` connection string

2. **Shared Secret**
   - Generate a strong secret for `BETTER_AUTH_SECRET` (minimum 32 characters)
   - Example: Use `openssl rand -base64 32` or an online password generator

3. **Monorepo Structure**
   - Root repository: `hackathon-todo/`
   - Create directories:
     - `/specs` (with subdirs: `phase1/`, `phase2/`, `features/`, `api/`, `database/`, `ui/`)
     - `/backend`
     - `/frontend`
   - Add `.spec-kit/config.yaml` with proper configuration
   - Add root `CLAUDE.md` with general instructions:
     ```
         "All development must use spec-driven methodology. Generate implementation code
         by reading specifications from /specs directory and following them precisely."
     ```

4. **Tools Required**
   - UV for Python project management
   - Node.js/npm/pnpm for frontend
   - Git for version control
   - Postman or curl for API testing
   - Docker and Docker Compose (for integration)
   - Screen recording tool (for demo video)

---

## Implementation Steps

### Step 1: Amend the Constitution for Phase 2

**Objective**: Update the project constitution to reflect Phase 2 requirements and establish governance for the full-stack architecture.

**Why First?** The constitution governs the entire project. Amending it ensures all specifications align with Phase 2 requirements (tech stack, authentication, monorepo structure, security policies).

**What to Do**:
1. Use the Constitution Amendment Prompt from the Phase 2 specification
2. Provide the existing Phase 1 constitution as context
3. Request Claude Code to generate the amended constitution

**Claude Code Interaction**:
```
PROMPT: "Generate an amended constitution for Phase 2 based on this specification.
         Incorporate full-stack requirements, JWT authentication, user isolation,
         and monorepo structure while preserving Spec-Driven Development principles."
```

**Refinement Tips**:
- **If sections are missing**: Add explicit instruction: "Include sections on Security, Monorepo Structure, and Technology Stack"
- **If auth details are vague**: Specify: "Detail JWT verification flow using BETTER_AUTH_SECRET environment variable"
- **If phase distinction unclear**: Request: "Clearly separate Phase 1 and Phase 2 requirements"
- **Review for completeness**: Ensure all 5 Basic Level features are documented

**Testing/Validation**:
1. Save amended constitution as `CONSTITUTION.md` in root
2. Read through document to verify:
   - ✅ Technology stack specified (Next.js, FastAPI, SQLModel, Neon, Better Auth)
   - ✅ API endpoints documented with {user_id} routing
   - ✅ JWT authentication requirements included
   - ✅ User isolation principles stated
   - ✅ Monorepo structure defined
   - ✅ Spec-Driven Development principles preserved
3. Commit to GitHub with message: "Amend constitution for Phase 2 full-stack implementation"

**Timeline Estimate**: 30-60 minutes

**Deliverables**:
- `CONSTITUTION.md` (updated for Phase 2)
- Git commit with amendment

---

### Step 2: Implement Section 1 - Backend

**Objective**: Build a fully functional FastAPI backend with Neon PostgreSQL persistence, JWT verification, and secure RESTful API endpoints.

**Why This Order?** Backend must be testable independently before frontend development. It handles data persistence, authentication verification, and user isolation—core requirements that frontend depends on.

**What to Do**:
1. Use the Backend Implementation Specification (Phase 2 Section 1)
2. Request Claude Code to generate complete backend code
3. Set up project structure in `/backend` directory

**Claude Code Interaction**:
```
PROMPT: "You are Claude Code. Generate the complete backend implementation as specified
         in the Phase 2 Section 1 specification. Output should be structured Markdown
         with each file in a separate code block, including file paths and full implementation."
```

**Implementation Steps**:
1. Navigate to `/backend` directory
2. Initialize UV project: `uv init`
3. Install dependencies: `uv add fastapi uvicorn sqlmodel pydantic python-jose asyncpg`
4. Add dev dependencies: `uv add --dev pytest pytest-asyncio black ruff`
5. Create `/backend/.env` file with:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require
   BETTER_AUTH_SECRET=your-secret-here
   TODO_HOST=0.0.0.0
   TODO_PORT=8000
   TODO_DEBUG=true
   ```
6. Generate code files from Claude Code output
7. Create database tables: Run `uv run python -c "from src.database import init_db; import asyncio; asyncio.run(init_db())"`

**Refinement Tips**:

| Issue | Refinement Prompt |
|-------|-------------------|
| Missing fields in Task model | "Update Task model to include created_at and updated_at datetime fields" |
| JWT verification fails | "Use python-jose library with HS256 algorithm for token verification" |
| Database connection errors | "Ensure asyncpg driver is used with SSL required for Neon PostgreSQL" |
| Syntax errors | "Fix syntax error in [file.py]: [paste error message]" |
| Endpoints not filtering by user_id | "Update all database queries to filter by user_id parameter" |

**Common Errors and Solutions**:
- **Error**: `ModuleNotFoundError: No module named 'src'`
  - **Solution**: Ensure running from `/backend` directory with proper Python path
- **Error**: `sqlalchemy.exc.ProgrammingError: relation "task" does not exist`
  - **Solution**: Run database initialization script to create tables
- **Error**: `JWTError: Signature verification failed`
  - **Solution**: Verify BETTER_AUTH_SECRET matches between .env and token generation
- **Error**: `asyncpg.exceptions.InvalidAuthorizationSpecificationError`
  - **Solution**: Ensure DATABASE_URL includes `?sslmode=require` for Neon

**Testing/Validation**:

1. **Start the server**:
   ```bash
   uv run uvicorn src.main:app --reload --port 8000
   ```

2. **Generate test JWT token**:
   - Use [jwt.io](https://jwt.io) with:
     - Algorithm: HS256
     - Secret: Your BETTER_AUTH_SECRET
     - Payload: `{"sub": "test_user_123", "exp": 1736000000}`
   - Copy the generated token

3. **Test endpoints with curl/Postman**:

   **Create Task**:
   ```bash
   curl -X POST http://localhost:8000/api/test_user_123/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Task", "description": "Test description"}'
   ```

   **List Tasks**:
   ```bash
   curl -X GET http://localhost:8000/api/test_user_123/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

   **Create task for different user**:
   ```bash
   # Should fail with 404 when trying to access other user's tasks
   curl -X GET http://localhost:8000/api/other_user_456/tasks/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

4. **Verify in Neon Console**:
   - Log into [Neon Console](https://console.neon.tech)
   - Navigate to your project
   - Open SQL Editor and run: `SELECT * FROM task;`
   - Verify tasks are saved with correct user_id

5. **Test authentication**:
   - Request without Authorization header → Should return 403
   - Request with invalid token → Should return 401
   - Request with valid token → Should succeed

6. **Test user isolation**:
   - Create task as user A
   - Try to access/update/delete as user B → Should return 404

**Deliverables**:
- Complete `/backend` directory with all source files
- Working API with all 6 endpoints
- Database schema created in Neon
- Test JWT tokens working
- Updated specifications in `/specs/api/rest-endpoints.md`
- Updated specifications in `/specs/database/schema.md`
- Git commits for all backend code

**Timeline Estimate**: 2-4 hours (including testing)

---

### Step 3: Implement Section 2 - Frontend

**Objective**: Build a responsive Next.js frontend with Better Auth authentication, JWT token management, and mock data implementation.

**Why After Backend?** Frontend can use mock data initially, but Better Auth configuration must align with backend JWT verification. Proceed only after backend is functional and JWT format is confirmed.

**What to Do**:
1. Use the Frontend Implementation Specification (Phase 2 Section 2)
2. Request Claude Code to generate complete frontend code
3. Set up Next.js project in `/frontend` directory

**Claude Code Interaction**:
```
PROMPT: "You are Claude Code. Generate the complete frontend implementation as specified
         in the Phase 2 Section 2 specification. Use Next.js 16+ with App Router,
         TypeScript, Better Auth with JWT plugin, and Tailwind CSS. Output should be
         structured Markdown with each file in a separate code block."
```

**Implementation Steps**:
1. Navigate to `/frontend` directory
2. Create Next.js app: `npx create-next-app@latest . --typescript --tailwind --app`
3. Install dependencies:
   ```bash
   npm install better-auth @better-auth/nextjs
   npm install axios
   ```
4. Create `/frontend/.env.local` with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-secret-here
   BETTER_AUTH_URL=http://localhost:3000
   ```
5. Better Auth configuration:
   ```bash
   npm install better-auth @better-auth/cli
   npx better-auth init
   ```
6. Configure Better Auth with JWT plugin in `lib/auth.ts`:
   ```typescript
   import { betterAuth } from "better-auth";
   import { jwt } from "better-auth/plugins";

   export const auth = betterAuth({
     database: {
       provider: "postgresql",
       url: process.env.DATABASE_URL!,
     },
     plugins: [
       jwt({
         issuer: "todo-app",
         expiration: 7 * 24 * 60 * 60, // 7 days
       }),
     ],
   });
   ```
7. Generate frontend code from Claude Code output
8. Implement mock data for initial testing

**Refinement Tips**:

| Issue | Refinement Prompt |
|-------|-------------------|
| JWT not included in API calls | "Ensure all API requests include Authorization header with Bearer token from Better Auth" |
| UI not responsive | "Use Tailwind CSS responsive classes (sm:, md:, lg:) for mobile/desktop layout" |
| Mock data doesn't match backend | "Update mock task data structure to match backend TaskResponse schema" |
| Signup/signin not working | "Verify Better Auth configuration includes proper redirect URLs and session handling" |
| Protected routes accessible when logged out | "Add authentication check in middleware or use useEffect to redirect unauthenticated users" |

**Testing/Validation**:

1. **Start frontend server**:
   ```bash
   npm run dev
   ```
   Navigate to `http://localhost:3000`

2. **Test authentication flow**:
   - Click "Sign Up" → Create new account
   - Should redirect to dashboard after signup
   - Check browser DevTools > Application > Cookies
   - Should see `better-auth.session-token` cookie
   - Verify JWT token is issued (check Network tab for `/api/auth/session` response)

3. **Test mock data display**:
   - Dashboard should display sample tasks
   - Verify UI shows: title, description, completion status
   - Test marking tasks complete (toggle checkbox)
   - Test adding new task (form submission)
   - Verify updates reflect in UI

4. **Test responsive design**:
   - Open DevTools > Toggle device toolbar
   - Test on mobile (375px), tablet (768px), desktop (1024px+)
   - Verify layout adapts correctly
   - Check touch targets are appropriately sized

5. **Test protected routes**:
   - Log out
   - Try to access `/dashboard` directly → Should redirect to `/login`
   - Try to access `/tasks/new` directly → Should redirect to `/login`

6. **Test Better Auth JWT**:
   - After login, decode the JWT token from cookies
   - Verify payload contains `sub` (user_id)
   - Verify signature matches `BETTER_AUTH_SECRET`
   - Token should be valid for 7 days

**Deliverables**:
- Complete `/frontend` directory with all components and pages
- Functional authentication (signup/signin) with Better Auth
- JWT token generation and storage
- Mock data implementation for all CRUD operations
- Responsive UI with Tailwind CSS
- Protected routes with authentication guards
- Updated specifications in `/specs/ui/components.md`
- Updated specifications in `/specs/ui/pages.md`
- Updated specifications in `/specs/auth/flow.md`
- Git commits for all frontend code

**Timeline Estimate**: 2-4 hours (including testing)

---

### Step 4: Implement Section 3 - Full Integration

**Objective**: Connect frontend to backend API, replace mock data with real API calls, configure CORS, and create deployment setup.

**Why Last?** Requires both backend and frontend to be fully functional. Integration exposes real-world issues like CORS, authentication token passing, and error handling.

**What to Do**:
1. Use the Full Integration Specification (Phase 2 Section 3)
2. Update frontend to call backend API instead of mock data
3. Configure backend CORS to allow frontend origin
4. Create docker-compose.yml for local development

**Claude Code Interaction**:
```
PROMPT: "You are Claude Code. Update the existing frontend code to integrate with the backend API
         as specified in Phase 2 Section 3. Replace all mock data calls with actual API requests
         using axios/fetch with proper Authorization headers. Add CORS middleware to FastAPI backend.
         Generate docker-compose.yml for local development. Output changes in code blocks with file paths."
```

**Implementation Steps**:

1. **Backend CORS Configuration**:
   - Update `src/main.py` to add CORS middleware:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Frontend API Integration**:
   - Create `lib/api.ts` for API client configuration:
   ```typescript
   import axios from 'axios';
   import { authClient } from './auth-client';

   const api = axios.create({
     baseURL: process.env.NEXT_PUBLIC_API_URL,
   });

   api.interceptors.request.use(async (config) => {
     const session = await authClient.getSession();
     if (session?.token) {
       config.headers.Authorization = `Bearer ${session.token}`;
     }
     return config;
   });
   ```
   - Replace all mock data calls with actual API calls
   - Add error handling and loading states

3. **Docker Setup**:
   - Create `docker-compose.yml` in root:
   ```yaml
   version: '3.8'
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=${DATABASE_URL}
         - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
       volumes:
         - ./backend:/app
       depends_on:
         - db

     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       environment:
         - NEXT_PUBLIC_API_URL=http://localhost:8000
       volumes:
         - ./frontend:/app
         - /app/node_modules

     db:
       image: postgres:15
       environment:
         - POSTGRES_USER=todo
         - POSTGRES_PASSWORD=todo
         - POSTGRES_DB=todo
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

4. **Environment Synchronization**:
   - Ensure both `.env` files use same `BETTER_AUTH_SECRET`
   - Verify `DATABASE_URL` in backend `.env`
   - Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`

**Refinement Tips**:

| Issue | Refinement Prompt |
|-------|-------------------|
| CORS errors in browser | "Add CORS middleware to FastAPI allowing origin http://localhost:3000 with credentials" |
| API calls missing Authorization header | "Ensure axios interceptor adds Bearer token from Better Auth session to all requests" |
| Data not persisting | "Verify API endpoints are called with correct method/URL and data matches schema" |
| Frontend build errors | "Check that all mock data has been replaced and TypeScript types match API responses" |
| Docker containers not connecting | "Add depends_on and verify network settings in docker-compose.yml" |

**Testing/Validation**:

1. **Start with docker-compose** (after updating .env):
   ```bash
   docker-compose up --build
   ```

2. **End-to-End Testing**:
   - Open `http://localhost:3000`
   - Sign up for new account
   - Add a new task → Verify it appears in list
   - Check Neon console → Verify task saved in database with correct user_id
   - Update task title → Verify change persists after refresh
   - Mark task complete → Verify completion status updates
   - Delete task → Verify it's removed from database
   - Log out → Verify authentication clears
   - Sign in as different user → Should not see first user's tasks

3. **User Isolation Testing**:
   - User A: Create 3 tasks
   - User B: Create 2 different tasks
   - User A should only see their 3 tasks
   - User B should only see their 2 tasks
   - Try to access User A's tasks from User B's session → Should get 404

4. **Authentication Testing**:
   - Login → JWT token issued
   - API calls include Authorization header
   - Token expires after 7 days
   - Invalid token returns 401
   - No token returns 403

5. **Cross-Origin Testing**:
   - Frontend at localhost:3000
   - Backend at localhost:8000
   - Requests should succeed without CORS errors
   - Cookies should be sent with credentials

6. **Performance Testing**:
   - Add 50+ tasks
   - List view should load quickly (< 500ms)
   - No UI lag on interactions

**Deliverables**:
- Updated frontend with real API integration
- CORS configuration in backend
- `docker-compose.yml` for local development
- All CRUD operations working end-to-end
- User isolation verified
- Updated specifications:
  - `/specs/architecture/integration.md`
  - `/specs/deployment/docker.md`
  - `/specs/features/full-e2e.md`
- Git commits for integration changes

**Timeline Estimate**: 1-3 hours

---

### Step 5: Final Review, Bonus, and Submission

**Objective**: Ensure all requirements are met, add bonus features if time permits, and prepare final submission.

**What to Do**:
1. Review all specifications in `/specs` directory
2. Test complete application flow
3. Add bonus features (optional)
4. Deploy frontend to Vercel
5. Create demo video
6. Submit via Google Form

**Review Checklist**:

**Backend Requirements**:
- ✅ FastAPI with SQLModel working
- ✅ Neon PostgreSQL connected
- ✅ All 6 API endpoints implemented
- ✅ JWT verification working
- ✅ User isolation enforced
- ✅ Proper error handling (401, 404, etc.)

**Frontend Requirements**:
- ✅ Next.js 16+ with App Router
- ✅ TypeScript implementation
- ✅ Better Auth with JWT plugin
- ✅ Responsive UI (mobile/desktop)
- ✅ All 5 Basic Level features functional
- ✅ Protected routes

**Integration Requirements**:
- ✅ Frontend calls backend API
- ✅ JWT tokens passed correctly
- ✅ CORS configured
- ✅ Data persists in database
- ✅ User isolation maintained
- ✅ Docker compose works

**Documentation**:
- ✅ CONSTITUTION.md updated
- ✅ All specs in `/specs` directory
- ✅ README.md in root
- ✅ Backend README.md
- ✅ Frontend README.md

**Bonus Features (Optional)**:
- +50: Voice commands with Web Speech API (spec in `/specs/features/voice.md`)
- +100: Urdu language support
- +200: Collaborative features

**Adding Urdu Language Support**:

If implementing bonus:

```bash
# Create specification for i18n
PROMPT: "Add Urdu language support to the Next.js frontend using next-intl or
         similar i18n library. Include language toggle in UI. Generate implementation."
```

Implementation steps:
1. Install next-intl: `npm install next-intl`
2. Create locales: `/locales/en.json`, `/locales/ur.json`
3. Update components to use translations
4. Add language switcher in navigation
5. Test both languages

**Deployment**:

1. **Deploy Frontend to Vercel**:
   ```bash
   cd frontend
   vercel login
   vercel --prod
   ```
   - Set environment variables in Vercel dashboard
   - Add `NEXT_PUBLIC_API_URL` pointing to backend
   - Deploy and copy URL

2. **Prepare Backend for Production**:
   - Use production Neon database URL
   - Set `DEBUG=false`
   - Use strong secret for `BETTER_AUTH_SECRET`
   - Deploy to Render, Railway, or similar

3. **Create Demo Video**:
   - Keep under 90 seconds
   - Show: Signup → Add task → Mark complete → Update → Delete
   - Show user isolation (two accounts)
   - Show database persistence
   - Record screen with audio narration
   - Upload to YouTube/Vimeo or share via Loom

**Final Testing**:
1. Run full application in production mode
2. Test all 5 Basic Level features:
   - Add Task ✅
   - View Task List ✅
   - Update Task ✅
   - Delete Task ✅
   - Mark as Complete ✅
3. Verify authentication required
4. Verify user isolation
5. Check all specs are complete

**Submission**:

1. **Prepare Links**:
   - GitHub repository link (public)
   - Vercel deployment link
   - Demo video link (YouTube/Vimeo/Loom)
   - WhatsApp number for contact

2. **Google Form Submission**:
   - Title: "Phase 2 Submission: [Your Name]"
   - Include all links
   - Brief description of features
   - Mention any bonus features implemented

3. **Final Git Commit**:
   ```bash
   git add .
   git commit -m "Complete Phase 2 implementation: full-stack todo app with auth and persistent storage

   - FastAPI backend with Neon PostgreSQL
   - Next.js frontend with Better Auth
   - JWT authentication and user isolation
   - All 5 Basic Level features implemented
   - Docker compose for local development
   - Deployed to Vercel

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
   git push origin main
   ```

**Timeline Estimate**: 1 hour (excluding bonus features)

**Final Deliverables**:
- ✅ Complete codebase in GitHub
- ✅ Working production deployment
- ✅ 90-second demo video
- ✅ All specifications in `/specs` directory
- ✅ Submitted Google Form

---

## Success Metrics

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| **Backend API uptime** | 100% local, deployed | Uvicorn/Gunicorn logs |
| **All endpoints working** | 6/6 endpoints tested | Postman/curl test suite |
| **JWT auth functional** | 401 for invalid token | Auth test cases |
| **User isolation** | User A cannot access User B's tasks | Multi-user test |
| **Frontend responsive** | Works on mobile/tablet/desktop | Browser devtools testing |
| **E2E CRUD operations** | All 5 features work | Manual testing |
| **Data persistence** | Tasks survive restart | Neon console verification |
| **Docker compose** | Both services start | `docker-compose up` success |
| **Specs complete** | All specs in /specs | Directory review |
| **Bonus features** | If attempted | Feature checklist |

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Claude Code generates incorrect code | High | Medium | Iterative refinement; test each section |
| JWT auth issues | Medium | High | Test auth flow early; verify secret sync |
| Neon connection failures | Low | High | Verify SSL mode; check connection string |
| CORS issues | Medium | Medium | Configure CORS early; test cross-origin |
| Time overrun | Medium | High | Focus on Basic features first; bonuses last |
| Frontend build errors | Medium | Medium | Use TypeScript; fix type errors early |
| User isolation bugs | Low | Critical | Test with multiple users; verify filters |

---

## Specification Version Control

Track all specification iterations in `/specs/history/`:

```
/specs/
├── history/
│   ├── constitution-v2.0.md
│   ├── backend-spec-v2.0.md
│   ├── frontend-spec-v2.0.md
│   ├── integration-spec-v2.0.md
│   └── amendment-log.md
├── phase1/
│   └── constitution-v1.0.md
└── phase2/
    ├── constitution-v2.0.md
    ├── section1-backend-fastapi-sqlmodel.md
    ├── section2-frontend-nextjs-betterauth.md
    ├── section3-full-integration.md
    └── implementation-plan.md
```

**Amendment Log Template**:
```markdown
# Specification Amendments

| Date | Spec File | Version | Changes | Reason |
|------|-----------|---------|---------|--------|
| YYYY-MM-DD | backend.md | 2.1 | Added pagination | Performance requirement |
| YYYY-MM-DD | frontend.md | 2.1 | Fixed auth flow | JWT sync issue |
```

---

## Communication Protocol

When stuck during implementation:

1. **Document the Problem**:
   - Screenshot/error message
   - Steps to reproduce
   - Expected vs. actual behavior

2. **Refine Specification**:
   - Add clarification to relevant spec file
   - Increment version number
   - Re-run Claude Code with refined spec

3. **Test Iteratively**:
   - Make small changes
   - Test immediately
   - Verify fix before proceeding

4. **Ask for Help**:
   - Use hackathon Discord/forum with specific questions
   - Include: spec version, error details, attempted solutions

---

## Quick Reference Commands

### Backend
```bash
# Navigate to backend
cd backend

# Initialize UV
uv init

# Install dependencies
uv add fastapi uvicorn sqlmodel pydantic python-jose asyncpg

# Run development server
uv run uvicorn src.main:app --reload --port 8000

# Run tests
uv run pytest tests/ -v

# Format code
uv run black src/ tests/
uv run ruff check src/ tests/
```

### Frontend
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install better-auth @better-auth/nextjs axios

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Docker
```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Testing
```bash
# Generate JWT for testing
python -c "
import jwt
import datetime
token = jwt.encode({
    'sub': 'test_user',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
}, 'your-secret', algorithm='HS256')
print(token)
"

# Test API endpoint
curl -X GET http://localhost:8000/api/test_user/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Conclusion

This implementation plan provides a structured approach to completing Phase 2 of the "Evolution of Todo" project using spec-driven development with Claude Code. By following these sequential steps and iterating on specifications until correct output is achieved, you can build a fully functional full-stack web application without manual coding.

**Key Success Factors**:
- ✅ Start with constitution amendment
- ✅ Complete and test backend first
- ✅ Implement frontend with mock data
- ✅ Integrate and test end-to-end
- ✅ Focus on Basic Level features
- ✅ Test user isolation thoroughly
- ✅ Document all specifications
- ✅ Submit before deadline

**Next Steps**:
1. Start with Step 1: Amend Constitution
2. Track progress in git commits
3. Iterate specifications as needed
4. Test continuously
5. Deploy and submit

**Questions or Issues?**:
- Review specifications in `/specs/phase2/`
- Check Claude Code documentation
- Ask in hackathon community channels

Good luck with Phase 2!

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-15 | Claude Code | Initial implementation plan |

---

*This document is part of the Phase 2 specification suite for "The Evolution of Todo" hackathon project.*

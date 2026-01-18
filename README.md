# Todo Full-Stack Web Application - Phase II

A modern, full-stack todo application built with **Next.js 14**, **FastAPI**, **Neon Serverless PostgreSQL**, and **Better Auth** with JWT authentication. This is Phase 2 of "The Evolution of Todo" project, transforming the Phase 1 console application into a production-ready web application with persistent storage and multi-user support.

## 🎉 Project Status: **Phase 2 COMPLETE** ✅

- **Phase**: II (The Evolution of Todo)
- **Status**: Implementation Complete (v2.0.0)
- **Architecture**: Full-Stack Web Application
- **Deployment**: Ready for Production

## 🚀 Live Demo

**Frontend**: https://your-frontend-url.vercel.app  *(update with actual URL)*

**Backend API**: https://your-backend-url.onrender.com  *(update with actual URL)*

**API Documentation**: https://your-backend-url.onrender.com/docs

## 📹 Demo Video

**Watch the Demo**: [YouTube/Loom Video Link] *(update with actual video URL)*

## 🏗️ Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT plugin
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI 0.109.0+
- **Language**: Python 3.13+
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel with async support
- **Authentication**: JWT (python-jose)
- **Package Manager**: UV

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: Neon PostgreSQL (Serverless)
- **Deployment**: Vercel (Frontend), Render/Railway (Backend)
- **Version Control**: Git/GitHub

## ✨ Features Implemented

### Basic Level Features (5/5) ✅

1. **✅ Add Task** - Create new tasks with title and description
2. **✅ View Task List** - Display all user's tasks in dashboard
3. **✅ Update Task** - Edit task title and description
4. **✅ Delete Task** - Remove tasks with confirmation
5. **✅ Mark as Complete** - Toggle completion status

### Authentication Features
- **✅ User Registration** - Sign up with email/password
- **✅ User Login** - Sign in with credentials
- **✅ User Logout** - Sign out and clear session
- **✅ JWT Tokens** - Secure token-based authentication
- **✅ Protected Routes** - Dashboard requires authentication
- **✅ User Isolation** - Users can only access their own tasks

### Additional Features
- **✅ Persistent Storage** - Tasks saved to Neon PostgreSQL
- **✅ Responsive Design** - Works on desktop, tablet, and mobile
- **✅ Real-time Updates** - Immediate UI feedback
- **✅ Inline Editing** - Edit tasks without page reload
- **✅ Data Validation** - Client and server-side validation
- **✅ Error Handling** - Graceful error messages
- **✅ Loading States** - UI feedback during operations

### 🎁 Bonus Features (Completed)
- **✅ Voice Commands (+50 pts)** - Add tasks using voice input (Web Speech API)
- **✅ Urdu Language Support (+100 pts)** - Full UI translation with language toggle

## 📁 Project Structure

```
hackathon-todo/
├── CONSTITUTION.md                 # Project constitution
├── TESTING-GUIDE.md               # Comprehensive testing guide
├── DEPLOYMENT-GUIDE.md            # Deployment instructions
├── SUBMISSION-CHECKLIST.md        # Submission checklist
├── docker-compose.yml             # Docker orchestration
├── .env                           # Environment variables
├── .gitignore
│
├── specs/                         # Specifications
│   └── phase2/
│       ├── implementation-plan.md
│       └── section1-backend-fastapi-sqlmodel.md
│
├── backend/                       # FastAPI Backend
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── .env
│   ├── README.md
│   └── src/
│       ├── main.py                # FastAPI app entry
│       ├── config.py              # Configuration
│       ├── database.py            # Database connection
│       ├── models/                # SQLModel entities
│       ├── schemas/               # Pydantic schemas
│       ├── routers/               # API endpoints
│       ├── dependencies/          # Auth & DB deps
│       └── utils/                 # JWT utilities
│       └── tests/                 # Test suite
│
└── frontend/                      # Next.js Frontend
    ├── Dockerfile
    ├── package.json
    ├── next.config.js
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── .env.local
    └── src/
        ├── app/                   # Next.js app routes
        │   ├── layout.tsx
        │   ├── page.tsx           # Landing page
        │   ├── signin/            # Sign in page
        │   ├── signup/            # Sign up page
        │   └── dashboard/         # Dashboard (protected)
        ├── lib/                   # Utilities
        │   ├── auth.ts            # Better Auth config
        │   ├── api.ts             # API client
        │   ├── auth-context.tsx   # Auth context
        │   └── auth-guard.tsx     # Protected routes
        └── components/            # React components
```

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Desktop
- Node.js 18+ (for local development)
- Python 3.13+ (for local development)
- UV package manager (`pip install uv`)
- Neon account (free at neon.tech)

### Quick Start (Docker)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hackathon-todo
   ```

2. **Configure environment variables**:
   ```bash
   # Copy and edit .env
   cp .env.example .env

   # Edit .env with your values:
   # - DATABASE_URL (from Neon console)
   # - BETTER_AUTH_SECRET (generate with: openssl rand -base64 32)
   ```

3. **Build and run with Docker**:
   ```bash
   docker compose build
   docker compose up
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

**Backend**:
```bash
cd backend
cp .env.example .env
# Edit .env with your values

# Install dependencies
uv add fastapi uvicorn sqlmodel pydantic python-jose asyncpg

# Run development server
uv run uvicorn src.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
cp .env.local.example .env.local
# Edit .env.local with your values

# Install dependencies
npm install

# Run development server
npm run dev
```

## 🔧 API Endpoints

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/{user_id}/tasks` | List all tasks | ✅ Required |
| `POST` | `/api/{user_id}/tasks` | Create new task | ✅ Required |
| `GET` | `/api/{user_id}/tasks/{id}` | Get task details | ✅ Required |
| `PUT` | `/api/{user_id}/tasks/{id}` | Update task | ✅ Required |
| `DELETE` | `/api/{user_id}/tasks/{id}` | Delete task | ✅ Required |
| `PATCH` | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | ✅ Required |
| `GET` | `/health` | Health check | ❌ Public |

## 🔐 Authentication Flow

1. User signs up/signs in via Better Auth (frontend)
2. Better Auth generates JWT token with user_id in `sub` claim
3. Frontend stores token (in cookies by default)
4. Frontend includes token in `Authorization: Bearer <token>` header for API calls
5. Backend verifies token using `BETTER_AUTH_SECRET`
6. Backend extracts user_id from token
7. All database queries filter by user_id for isolation

**Security**: Users can only access, modify, or delete their own tasks.

## 🐳 Docker Commands

```bash
# Build all containers
docker compose build

# Start all services
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f
docker compose logs backend
docker compose logs frontend

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Restart specific service
docker compose restart backend

# Check status
docker compose ps
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
uv run pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Manual Testing Checklist

See [TESTING-GUIDE.md](./TESTING-GUIDE.md) for comprehensive testing instructions.

## 🚀 Deployment

### Deploy to Production

**Option 1: Docker Compose (Self-Hosted)**

```bash
# Edit .env with production values
docker compose build
docker compose up -d
```

**Option 2: Vercel (Frontend) + Render (Backend)**

See [DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md) for detailed deployment instructions.

**Quick Deploy**:

1. **Backend to Render**:
   ```bash
   # Connect GitHub repo to Render
   # Set environment variables in Render dashboard
   # Deploy automatically on push
   ```

2. **Frontend to Vercel**:
   ```bash
   npm i -g vercel
   cd frontend
   vercel --prod
   ```

## 📋 Specifications & Documentation

All development was guided by specifications following **Spec-Driven Development** principles:

- **CONSTITUTION.md** - Project principles and standards
- **specs/phase2/implementation-plan.md** - Step-by-step implementation plan
- **specs/phase2/section1-backend-fastapi-sqlmodel.md** - Backend specification
- **TESTING-GUIDE.md** - Comprehensive testing procedures
- **DEPLOYMENT-GUIDE.md** - Deployment instructions
- **SUBMISSION-CHECKLIST.md** - Submission requirements

## 🎓 Development Principles

This project follows **Spec-Driven Development**:

1. **No code without approved specifications**
2. **AI-native workflow** using Claude Code for generation
3. **Clean code** with type hints, documentation, and best practices
4. **Security-first** with JWT authentication and user isolation
5. **Testability** - Designed for easy testing
6. **Reproducibility** - Docker-based deployment

See [CONSTITUTION.md](./CONSTITUTION.md) for complete principles.

## 🐛 Troubleshooting

Common issues and solutions:

**Database Connection Failed**:
- Verify DATABASE_URL format includes `?sslmode=require`
- Check Neon project is active
- Ensure correct credentials

**JWT Authentication Failed**:
- Verify BETTER_AUTH_SECRET matches frontend and backend
- Check token hasn't expired
- Ensure user_id in URL matches JWT sub claim

**CORS Errors**:
- Update CORS origins in backend to include frontend URL
- Check NEXT_PUBLIC_API_URL is correct

See [DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md) for detailed troubleshooting.

## 📞 Support

For issues and questions:
1. Check [TESTING-GUIDE.md](./TESTING-GUIDE.md) for test procedures
2. Check [DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md) for deployment help
3. Review [CONSTITUTION.md](./CONSTITUTION.md) for project principles
4. Check logs: `docker compose logs`

## 🤝 Contributing

This is a Phase 2 project submission. For contributions:

1. Follow Spec-Driven Development principles
2. Update specifications before code changes
3. Add tests for new features
4. Ensure all tests pass
5. Update documentation

## 📄 License

MIT License - See LICENSE file for details.

## 🎯 Project Completion Status

| Phase | Status | Features |
|-------|--------|----------|
| **Phase I** | ✅ Complete | Console app, in-memory storage |
| **Phase II** | ✅ Complete | Full-stack, JWT auth, Neon DB |

**All 5 Basic Level Features**: ✅ Implemented
**Authentication**: ✅ Implemented
**Deployment**: ✅ Ready

---

**Built with ❤️ using Spec-Driven Development and Claude Code**

**Project Name**: Todo Full-Stack Web Application (Phase II: The Evolution of Todo)

**Technologies**: Next.js 14, TypeScript, FastAPI, Python 3.13, Neon PostgreSQL, Better Auth, Docker, JWT

**Status**: Ready for Submission 🚀

**Last Updated**: January 16, 2026

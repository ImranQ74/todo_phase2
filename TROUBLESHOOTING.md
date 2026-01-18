# Troubleshooting Guide - Todo Phase 2 Testing

## 🔍 Quick Diagnostic Commands

Run these first to identify issues:

```powershell
# From project root
cd "C:\Users\User\Desktop\to do project1"

# Check Python
cd backend
python --version
cd ..

# Check Node
cd frontend
node --version
cd ..

# Check environment
ls .env
cat .env
```

---

## ❌ Common Backend Errors

### Error 1: "ModuleNotFoundError: No module named 'uvicorn'"

**Symptoms**:
```
Traceback (most recent call last):
  File "...", line 1, in <module>
    import uvicorn
ModuleNotFoundError: No module named 'uvicorn'
```

**Causes**:
- Dependencies not installed
- Virtual environment not activated
- Wrong directory

**Solutions**:

1. **Install dependencies with UV**:
   ```powershell
   cd backend
   uv add fastapi uvicorn sqlmodel pydantic pydantic-settings python-jose asyncpg python-multipart httpx
   ```

2. **Install manually with pip**:
   ```powershell
   cd backend
   uv pip install -e .
   ```

3. **Use virtual environment**:
   ```powershell
   cd backend
   ..\.venv\Scripts\activate
   uv pip install fastapi uvicorn sqlmodel pydantic python-jose asyncpg
   ```

---

### Error 2: "ModuleNotFoundError: No module named 'src'"

**Symptoms**:
```
ModuleNotFoundError: No module named 'src'
```

**Causes**:
- Running from wrong directory
- Python path issue

**Solutions**:

1. **Run from backend directory** (NOT backend/src):
   ```powershell
   cd backend  # Correct
   uv run uvicorn src.main:app --reload
   ```

2. **Set Python path**:
   ```powershell
   cd backend
   set PYTHONPATH=.
   uv run uvicorn src.main:app --reload
   ```

---

### Error 3: "No module named 'asyncpg'"

**Symptoms**:
```
ModuleNotFoundError: No module named 'asyncpg'
```

**Causes**:
- PostgreSQL driver not installed
- Missing dependency for database connection

**Solutions**:

```powershell
cd backend
uv add asyncpg
```

---

### Error 4: "DATABASE_URL not configured"

**Symptoms**:
```
KeyError: 'DATABASE_URL'
ValidationError: DATABASE_URL is required
```

**Causes**:
- .env file missing
- .env file in wrong location
- Environment file not loaded

**Solutions**:

1. **Verify .env file exists**:
   ```powershell
   cd backend
   ls .env
   ```

2. **Create .env if missing**:
   ```powershell
   cd backend
   cp .env.example .env
   ```

3. **Check .env content**:
   ```powershell
   cat .env
   ```

   Should contain:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require
   BETTER_AUTH_SECRET=your-secret-here
   ```

4. **Verify TODO_ prefix variables**:
   ```
   TODO_DATABASE_URL=postgresql+asyncpg://...
   TODO_BETTER_AUTH_SECRET=your-secret
   ```

---

### Error 5: "asyncpg.exceptions.InvalidAuthorizationSpecificationError"

**Symptoms**:
```
sqlalchemy.exc.DBAPIError: (asyncpg.exceptions.InvalidAuthorizationSpecificationError) no pg_hba.conf entry
```

**Causes**:
- Neon requires SSL but not specified
- Incorrect connection URL format

**Solutions**:

**Edit `backend/.env`**:
```bash
# WRONG:
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/todo

# CORRECT (with sslmode):
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/todo?sslmode=require
```

---

### Error 6: "sqlalchemy.exc.ProgrammingError: relation 'task' does not exist"

**Symptoms**:
```
sqlalchemy.exc.ProgrammingError: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError) <class 'asyncpg.exceptions.UndefinedTableError'>: relation "task" does not exist
```

**Causes**:
- Database tables not created
- Database schema not initialized

**Solutions**:

**Option 1: Initialize database manually**:
```powershell
cd backend
python -c "
import asyncio
from src.database import init_db

async def setup():
    await init_db()
    print('Database tables created!')

asyncio.run(setup())
"
```

**Option 2: Add initialization to main.py**:
Add before `uvicorn.run()`:
```python
import asyncio
from src.database import init_db

asyncio.run(init_db())
```

---

### Error 7: "JWTError: Signature verification failed"

**Symptoms**:
```
jose.exceptions.JWTError: Signature verification failed
```

**Causes**:
- BETTER_AUTH_SECRET mismatched
- Secret too short (< 32 chars)
- Different secrets in frontend/backend

**Solutions**:

1. **Generate new secure secret**:
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update ALL .env files** with SAME secret:
   - Root `.env`
   - `backend/.env`
   - `frontend/.env.local`

3. **Verify secret length**:
   ```powershell
   python -c "
   from src.config import get_settings
   s = get_settings()
   print(f'Secret length: {len(s.better_auth_secret)} chars')
   print(f'Should be >= 32: {len(s.better_auth_secret) >= 32}')
   "
   ```

---

### Error 8: "ImportError: cannot import name 'BaseModel' from 'pydantic'"

**Symptoms**:
```
ImportError: cannot import name 'BaseModel' from 'pydantic'
```

**Causes**:
- Pydantic v1 vs v2 compatibility issue

**Solutions**:

```powershell
cd backend
uv add "pydantic>=2.5.0" "pydantic-settings>=2.1.0"
```

---

## ❌ Common Frontend Errors

### Error 1: "'npm' is not recognized"

**Symptoms**:
```
npm : The term 'npm' is not recognized as the name of a cmdlet
```

**Causes**:
- Node.js not installed
- Node.js not in PATH

**Solutions**:

1. **Install Node.js**:
   - Download from https://nodejs.org/
   - Install Node.js 18+ (LTS version)
   - Restart PowerShell

2. **Verify installation**:
   ```powershell
   node --version
   npm --version
   ```

---

### Error 2: "Failed to compile: Module not found"

**Symptoms**:
```
Module not found: Can't resolve 'better-auth'
Module not found: Can't resolve 'axios'
```

**Causes**:
- Dependencies not installed
- node_modules missing

**Solutions**:

```powershell
cd frontend
npm install
```

If errors persist:
```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

### Error 3: "TypeError: Cannot read property 'use' of undefined"

**Symptoms**:
```
TypeError: Cannot read property 'use' of undefined
```

**Causes**:
- axios not properly imported
- Circular dependency

**Solutions**:

Check `frontend/src/lib/api.ts`:
```typescript
import axios from 'axios'  // NOT: import { axios } from 'axios'
```

---

### Error 4: "CORS error: No 'Access-Control-Allow-Origin' header"

**Symptoms**:
```
Access to XMLHttpRequest blocked by CORS policy
```

**Causes**:
- Backend CORS not configured
- Frontend calling wrong port
- Backend not running

**Solutions**:

**1. Verify backend is running**:
```powershell
# In backend directory
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

**2. Update CORS in backend/src/main.py**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Add this
        "*"  # Or wildcard for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**3. Restart backend** after changing CORS

---

### Error 5: "useAuth must be used within AuthProvider"

**Symptoms**:
```
Error: useAuth must be used within AuthProvider
```

**Causes**:
- Component using useAuth() outside AuthProvider
- Missing AuthProvider wrapper

**Solutions**:

**Check frontend/src/app/layout.tsx**:
```typescript
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>  {/* MUST wrap everything */}
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
```

---

### Error 6: "Error: Could not find a declaration file for module 'better-auth'"

**Symptoms**:
```
Could not find a declaration file for module 'better-auth'
```

**Causes**:
- Missing TypeScript types
- better-auth not installed

**Solutions**:

**1. Install better-auth**:
```powershell
cd frontend
npm install better-auth @better-auth/nextjs
```

**2. Create type declaration file** (`frontend/src/types/better-auth.d.ts`):
```typescript
declare module 'better-auth';
declare module '@better-auth/nextjs';
```

---

## 🔌 Integration Errors

### Error 1: "GET http://localhost:8000/api/{user_id}/tasks 401 (Unauthorized)"

**Symptoms**:
```
GET http://localhost:8000/api/test-user-123/tasks 401 (Unauthorized)
```

**Causes**:
- JWT token not sent
- Token expired or invalid
- Wrong secret

**Solutions**:

**1. Verify token is sent in frontend**:
```typescript
// In frontend/src/lib/api.ts
api.interceptors.request.use(async (config) => {
  const session = await authClient.getSession()
  if (session?.token) {
    config.headers.Authorization = `Bearer ${session.token}`  // Must be present
  }
  return config
})
```

**2. Verify token format**:
```javascript
// Check browser DevTools > Application > Cookies
// Look for session token from Better Auth
```

**3. Decode token to verify**:
```powershell
cd backend
python -c "
from src.utils.jwt import decode_jwt
import sys
token = 'YOUR_TOKEN_HERE'
payload = decode_jwt(token)
print(payload)
"
```

---

### Error 2: "TypeError: Cannot read properties of undefined (reading 'map')"

**Symptoms**:
```
TypeError: Cannot read properties of undefined (reading 'map')
```

**Causes**:
- API returning error instead of data
- tasks is undefined

**Solutions**:

**Check API response format**:
```typescript
// Frontend expects: { tasks: [...], total: n }
// If API returns array directly, update frontend

// WRONG:
const tasks = response.data.map(...)

// CORRECT:
const tasks = response.data.tasks.map(...)
```

**Add error handling**:
```typescript
try {
  const response = await taskAPI.list(userId)
  if (response.tasks) {
    setTasks(response.tasks)
  }
} catch (error) {
  console.error('Failed to load tasks:', error)
  setTasks([])  // Set empty array on error
}
```

---

### Error 3: "NetworkError when attempting to fetch resource"

**Symptoms**:
```
NetworkError when attempting to fetch resource
```

**Causes**:
- Backend not running
- Wrong port
- Firewall blocking

**Solutions**:

1. **Verify backend is running**:
   ```powershell
   netstat -ano | findstr :8000
   # Should show LISTENING
   ```

2. **Check port availability**:
   ```powershell
   # Kill process on port 8000 if needed
timeout /t 5
cd "C:\Users\User\Desktop\to do project1\backend"
echo Testing backend configuration...

REM Check if .venv exists
if exist .\.venv\Scripts\python.exe (
    set PYTHON_CMD=.\.venv\Scripts\python.exe
) else (
    set PYTHON_CMD=python
)

REM Create test script
echo import asyncio > test_backend.py
echo from src.config import get_settings >> test_backend.py
echo from src.utils.jwt import create_jwt >> test_backend.py
echotask," tests remaining incomplete as model finishes the current tool call. The user wants help troubleshooting testing errors. I'll create a comprehensive troubleshooting script that checks all common issues.
# Environment Configuration & Testing Guide

## Quick Setup Steps

### 1. Generate a Secure Secret

Run this command in PowerShell to generate a JWT secret:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Example output**: `FE4FJu7xKO0dCDEwlEU8b0QmlbVv93eMScOVWiId0t4`

### 2. Update Environment Files

**File: `.env` (in project root)**
```bash
# Replace this line:
# DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require

# With your actual Neon URL (get from https://console.neon.tech):
DATABASE_URL=postgresql+asyncpg://your-user:your-password@ep-xxx.region.neon.tech/todo?sslmode=require

# Replace this line:
# BETTER_AUTH_SECRET=your-256-bit-secret-key-here-at-least-32-chars-change-this

# With the generated secret:
BETTER_AUTH_SECRET=YOUR_GENERATED_SECRET_HERE
BETTER_AUTH_ALGORITHM=HS256
TODO_HOST=0.0.0.0
TODO_PORT=8000
TODO_DEBUG=true
```

**File: `backend/.env`**
```bash
# Same content as root .env
DATABASE_URL=postgresql+asyncpg://your-user:your-password@ep-xxx.region.neon.tech/todo?sslmode=require
BETTER_AUTH_SECRET=YOUR_GENERATED_SECRET_HERE
BETTER_AUTH_ALGORITHM=HS256
TODO_HOST=0.0.0.0
TODO_PORT=8000
TODO_DEBUG=true
```

**File: `frontend/.env.local`**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=YOUR_GENERATED_SECRET_HERE
BETTER_AUTH_URL=http://localhost:3000
```

### 3. Get Neon Database URL

1. Sign up at https://neon.tech
2. Create a new project
3. Navigate to your project dashboard
4. Click "Connect" on your database
5. Copy the connection string
6. Replace in the .env files above

## Testing Without Docker

### Test Backend (Python)

From PowerShell:

```powershell
cd "C:\Users\User\Desktop\to do project1\backend"

# Install dependencies if not already done
uv add fastapi uvicorn sqlmodel pydantic pydantic-settings python-jose asyncpg python-multipart httpx

# Test configuration
python -c "
import asyncio
from src.config import get_settings
from src.utils.jwt import create_jwt, decode_jwt

async def test():
    s = get_settings()
    print(f'Database: {s.database_url[0:30]}...')
    print(f'Secret: {len(s.better_auth_secret)} chars')
    print(f'Algorithm: {s.better_auth_algorithm}')

    # Test JWT
    token = create_jwt('test-user-123')
    print(f'Token: {token[0:30]}...')
    payload = decode_jwt(token)
    print(f'Payload: sub={payload.get(\"sub\")}')

asyncio.run(test())
"
```

### Run Backend Server

```powershell
# From backend directory
uv run uvicorn src.main:app --reload --port 8000
```

Then test:
- Health check: http://localhost:8000/health (should show {"status": "healthy"})
- API docs: http://localhost:8000/docs (Swagger UI)

### Test Frontend

From a new PowerShell window:

```powershell
cd "C:\Users\User\Desktop\to do project1\frontend"

# Install dependencies if not already done
npm install

# Run dev server
npm run dev
```

Then open: http://localhost:3000

### Test Full Integration

1. Open http://localhost:3000 in browser
2. Click "Sign Up"
3. Create account (email/password)
4. Should redirect to dashboard
5. Try to add a task
6. Check if task appears and persists
7. Check browser DevTools > Network tab
8. Verify API calls include Authorization header

## Common Issues

### Issue: "No module named 'src'"
**Solution**: Run commands from the `backend` directory, not `backend/src`

### Issue: "Database connection failed"
**Solution**:
- Verify DATABASE_URL format includes `?sslmode=require`
- Check Neon project is active
- Ensure your IP is whitelisted in Neon dashboard

### Issue: "JWTError: Signature verification failed"
**Solution**:
- Ensure BETTER_AUTH_SECRET matches in all 3 .env files
- Must be at least 32 characters

### Issue: "ModuleNotFoundError: No module found"
**Solution**:
- Run `uv add fastapi uvicorn sqlmodel pydantic python-jose asyncpg`
- Or use the virtual environment: `.\.venv\Scripts\activate`

### Issue: "Port already in use"
**Solution**:
- Change port: `uvicorn src.main:app --reload --port 8001`
- Or kill process using the port

## Expected Test Results

✅ **Backend Tests**:
```
Health check: ✓ Returns {"status": "healthy"}
JWT token: ✓ Generated and verified
Database: ✓ Configuration loaded
API docs: ✓ Swagger UI accessible
```

✅ **Frontend Tests**:
```
Landing page: ✓ Loads at http://localhost:3000
Sign up: ✓ Form displays and validates
Sign in: ✓ Form displays and validates
Dashboard: ✓ Protected route redirects if not authenticated
API calls: ✓ Include Authorization header
```

✅ **Integration Tests**:
```
Create task: ✓ Task saved to database
List tasks: ✓ All user's tasks displayed
Update task: ✓ Changes persist
Delete task: ✓ Task removed from database
Toggle complete: ✓ Status changes correctly
User isolation: ✓ Cannot access other users' tasks
```

## Next Steps

1. ✅ Environment configured
2. ✅ Backend tested locally
3. ✅ Frontend tested locally
4. 🔄 Docker Compose test (requires Docker Desktop)
5. 🔄 Production deployment to Vercel & Render
6. 🔄 Record demo video
7. 🔄 Submit to Google Form

## Need Help?

See TESTING-GUIDE.md for comprehensive testing procedures.

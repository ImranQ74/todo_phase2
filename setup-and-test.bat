@echo off
REM Setup and Test Script for Todo Phase 2 Project
REM This script configures environment and runs local tests

echo ==========================================
echo Todo Phase 2 - Setup & Test Script
echo ==========================================
echo.

REM Check Python availability
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.13 or higher
    pause
    exit /b 1
)

echo ✅ Python is available
echo.

REM Step 1: Generate secure secret
echo STEP 1: Generating secure JWT secret...
for /f "tokens=*" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set JWT_SECRET=%%i
echo ✅ Generated JWT secret: %JWT_SECRET:~0,20%...
echo.

REM Step 2: Configure environment files
echo STEP 2: Configuring environment files...

REM Check if Neon URL is already set in .env
findstr /C:"DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx" .env >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  WARNING: .env contains placeholder DATABASE_URL
    echo Please update .env with your actual Neon URL before testing
    echo.
    echo Instructions:
    echo 1. Go to https://console.neon.tech
    echo 2. Create a project or select existing
    echo 3. Copy the connection string
    echo 4. Replace DATABASE_URL in .env
    echo.
    echo Press any key to continue with placeholder (tests will fail)...
    pause >nul
)

REM Update .env file with generated secret
echo # Auto-generated configuration > .env.new
echo DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require >> .env.new
echo BETTER_AUTH_SECRET=%JWT_SECRET% >> .env.new
echo BETTER_AUTH_ALGORITHM=HS256 >> .env.new
echo TODO_HOST=0.0.0.0 >> .env.new
echo TODO_PORT=8000 >> .env.new
echo TODO_DEBUG=true >> .env.new
move /Y .env.new .env >nul
echo ✅ Updated root .env
echo.

REM Update backend .env
if exist backend\.env.example (
    echo # Auto-generated backend configuration > backend\.env.new
echo DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require >> backend\.env.new
echo BETTER_AUTH_SECRET=%JWT_SECRET% >> backend\.env.new
echo BETTER_AUTH_ALGORITHM=HS256 >> backend\.env.new
echo TODO_HOST=0.0.0.0 >> backend\.env.new
echo TODO_PORT=8000 >> backend\.env.new
echo TODO_DEBUG=true >> backend\.env.new
move /Y backend\.env.new backend\.env >nul
echo ✅ Updated backend .env
) else (
    echo ⚠️  backend/.env.example not found, skipping backend .env
)
echo.

REM Update frontend .env.local
echo # Auto-generated frontend configuration > frontend\.env.local.new
echo NEXT_PUBLIC_API_URL=http://localhost:8000 >> frontend\.env.local.new
echo BETTER_AUTH_SECRET=%JWT_SECRET% >> frontend\.env.local.new
echo BETTER_AUTH_URL=http://localhost:3000 >> frontend\.env.local.new
move /Y frontend\.env.local.new frontend\.env.local >nul
echo ✅ Updated frontend .env.local
echo.

REM Step 3: Check Docker
echo STEP 3: Checking Docker installation...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Docker not found! Please install Docker Desktop
    echo You can still test the backend locally without Docker
    echo.
    set DOCKER_AVAILABLE=false
) else (
    echo ✅ Docker is available
    set DOCKER_AVAILABLE=true
)
echo.

REM Step 4: Test Backend (Python) locally
echo STEP 4: Testing Backend configuration...
cd backend

REM Check if dependencies are installed
if exist .\.venv\Scripts\python.exe (
    echo ✅ UV virtual environment found
) else (
    echo Installing backend dependencies...
    uv add fastapi uvicorn sqlmodel pydantic pydantic-settings python-jose asyncpg python-multipart httpx pytest pytest-asyncio black ruff 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo ⚠️  Failed to install some dependencies (non-critical)
    )
    echo.
)

REM Create simple test script
echo import asyncio > test_config.py
echo from src.config import get_settings >> test_config.py
echo from src.utils.jwt import create_jwt, decode_jwt >> test_config.py
echo. >> test_config.py
echo async def test_config(): >> test_config.py
echo     settings = get_settings() >> test_config.py
echo     print(f"✅ Database URL configured: {settings.database_url[0:20]}...") >> test_config.py
echo     print(f"✅ Auth secret configured: {len(settings.better_auth_secret)} chars") >> test_config.py
echo     print(f"✅ Algorithm: {settings.better_auth_algorithm}") >> test_config.py
echo     return True >> test_config.py
echo. >> test_config.py
echo async def test_jwt(): >> test_config.py
echo     token = create_jwt("test-user-123") >> test_config.py
echo     print(f"✅ JWT token generated: {token[0:30]}...") >> test_config.py
echo     payload = decode_jwt(token) >> test_config.py
echo     print(f"✅ JWT payload: sub={payload.get('sub')}") >> test_config.py
echo     return True >> test_config.py
echo. >> test_config.py
echo if __name__ == "__main__": >> test_config.py
echo     asyncio.run(test_config()) >> test_config.py
echo     asyncio.run(test_jwt()) >> test_config.py

REM Run the test
echo Running backend configuration tests...
if exist .\.venv\Scripts\python.exe (
    .\.venv\Scripts\python.exe test_config.py
) else (
    python test_config.py
)
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Configuration test failed
)
del test_config.py
cd ..
echo.

REM Step 5: Summary
echo ==========================================
echo ✅ Setup Complete!
echo ==========================================
echo.
echo Next Steps:
echo 1. TODO: Add your DATABASE_URL to .env (get from https://console.neon.tech)
echo 2. Start services with: docker compose up
echo 3. Test frontend: http://localhost:3000
echo 4. Test backend API: http://localhost:8000/docs
echo 5. Run backend tests: cd backend ^& uv run pytest tests/
echo.
echo 📝 TESTING-GUIDE.md has comprehensive test procedures
echo.
echo Press any key to view final configuration summary...
pause >nul

REM Show summary
echo.
echo ==========================================
echo Configuration Summary
echo ==========================================
echo.
type .env
echo.
echo ✅ Setup complete!
echo.
echo REMEMBER: Update DATABASE_URL in .env before running!
echo.
pause

@echo off
REM Backend Dependencies Installation Script
REM Run this from the backend directory

echo ==========================================
echo Installing Backend Dependencies
echo ==========================================
echo.

REM Check if UV is available
where uv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: UV not found!
    echo Please install UV: pip install uv
    pause
    exit /b 1
)

echo ✅ UV is available
echo.

REM Install core dependencies one by one with error handling
echo Installing FastAPI...
uv add fastapi
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: FastAPI install had issues
)
echo.

echo Installing Uvicorn...
uv add uvicorn
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: Uvicorn install had issues
)
echo.

echo Installing SQLModel...
uv add sqlmodel
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: SQLModel install had issues
)
echo.

echo Installing Pydantic and extensions...
uv add pydantic pydantic-settings
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: Pydantic install had issues
)
echo.

echo Installing Python-JOSE with cryptography...
uv add "python-jose[cryptography]"
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: Python-JOSE install had issues
)
echo.

echo Installing AsyncPG (PostgreSQL driver)...
uv add asyncpg
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: AsyncPG install had issues
)
echo.

echo Installing Python-Multipart (for form data)...
uv add python-multipart
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: Python-Multipart install had issues
)
echo.

echo Installing HTTPX (HTTP client)...
uv add httpx
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: HTTPX install had issues
)
echo.

echo Installing development dependencies...
uv add --dev pytest pytest-asyncio pytest-cov black ruff mypy
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Warning: Dev dependencies install had issues
)
echo.

echo ==========================================
echo Dependency Installation Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Check for any warnings above
echo 2. Update DATABASE_URL in .env file with Neon URL
echo 3. Run: uv run uvicorn src.main:app --reload --port 8000
echo.
pause

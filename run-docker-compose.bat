@echo off
REM Windows script to setup and run docker-compose for the Todo app

echo ============================================
echo Todo App - Docker Compose Setup & Run
echo ============================================
echo.

REM Step 1: Check Docker is running
echo Checking if Docker is running...
docker version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not running or not installed!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo Docker is running.
echo.

REM Step 2: Check .env files exist
echo Checking for .env files...
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create .env from .env.example
    echo.
    pause
    exit /b 1
)

if not exist backend\.env (
    echo Copying backend .env.example to .env...
    copy backend\.env.example backend\.env
)

if not exist frontend\.env.local (
    echo Copying frontend .env.local.example to .env.local...
    copy frontend\.env.local.example frontend\.env.local
)

REM Step 3: Generate a secure secret if not already set
echo Checking for BETTER_AUTH_SECRET...
findstr "BETTER_AUTH_SECRET=your-256-bit" .env >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo.
    echo WARNING: Default BETTER_AUTH_SECRET detected!
    echo Generating a secure secret...
    echo.

    REM Generate new secret using PowerShell
    for /f "tokens=*" %%i in ('powershell -Command "-join ((65..90) + (97..122) | Get-Random -Count 32 | %%{[char]$_})"
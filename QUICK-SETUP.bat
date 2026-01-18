@echo off
REM Quick Setup Script - Configure environment for testing

echo ==========================================
echo TODO PHASE 2 - QUICK SETUP
echo ==========================================
echo.

REM Step 1: Generate secret
echo Generating secure JWT secret...
for /f "tokens=*" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set JWT_SECRET=%%i
echo Secret: %JWT_SECRET:~0,30%...
echo.

REM Step 2: Check for placeholder in root .env
echo Checking root .env configuration...
findstr "user:password@ep-xxx" .env >nul 2>&1
if %ERRORLEVEL%==0 (
    echo WARNING: Root .env has placeholder DATABASE_URL
    echo Please update with actual Neon URL from https://console.neon.tech
    echo.
) else (
    echo Root .env DATABASE_URL appears to be configured
)

findstr "your-256-bit-secret" .env >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Updating root .env BETTER_AUTH_SECRET...
    echo DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require > .env.new
echo BETTER_AUTH_SECRET=%JWT_SECRET% >> .env.new
echo BETTER_AUTH_ALGORITHM=HS256 >> .env.new
echo TODO_HOST=0.0.0.0 >> .env.new
echo TODO_PORT=8000 >> .env.new
echo TODO_DEBUG=true >> .env.new
echo POSTGRES_USER=todo_user >> .env.new
echo POSTGRES_PASSWORD=todo_password >> .env.new
echo POSTGRES_DB=todo_db >> .env.new
move /Y .env.new .env >nul
    echo Updated root .env
) else (
    echo Root .env BETTER_AUTH_SECRET appears to be configured
)
echo.

REM Step 3: Update backend .env
echo Checking backend .env...
if exist backend\.env (
    findstr "your-256-bit-secret" backend\.env >nul 2>&1
    if %ERRORLEVEL%==0 (
        echo Updating backend .env BETTER_AUTH_SECRET...
        echo DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/todo?sslmode=require > backend\.env.new
echo BETTER_AUTH_SECRET=%JWT_SECRET% >> backend\.env.new
echo BETTER_AUTH_ALGORITHM=HS256 >> backend\.env.new
echo TODO_HOST=0.0.0.0 >> backend\.env.new
echo TODO_PORT=8000 >> backend\.env.new
echo TODO_DEBUG=true >> backend\.env.new
move /Y backend\.env.new backend\.env >nul
        echo Updated backend .env
    ) else (
        echo Backend .env appears to be configured
    )
) else (
    echo Backend .env does not exist
)
echo.

REM Step 4: Update frontend .env.local
echo Checking frontend .env.local...
if exist frontend\.env.local (
    findstr "your-256-bit-secret" frontend\.env.local >nul 2>&1
    if %ERRORLEVEL%==0 (
        echo Updating frontend .env.local...
        echo NEXT_PUBLIC_API_URL=http://localhost:8000 > frontend\.env.local.new
echo BETTER_AUTH_SECRET=%JWT_SECRET% >> frontend\.env.local.new
echo BETTER_AUTH_URL=http://localhost:3000 >> frontend\.env.local.new
move /Y frontend\.env.local.new frontend\.env.local >nul
        echo Updated frontend .env.local
    ) else (
        echo Frontend .env.local appears to be configured
    )
) else (
    echo Frontend .env.local does not exist
)
echo.

REM Step 5: Summary
echo ==========================================
echo SETUP COMPLETE
echo ==========================================
echo.
echo Configuration summary:
echo - JWT Secret: Generated and set in all .env filesecho - Database URL: Placeholder (you need to update this)
echo.
echo FILES UPDATED:
echo - .env (root)
echo - backend\.env
echo - frontend\.env.local
echo.
echo NEXT STEPS:
echo 1. Sign up at https://neon.tech
echo 2. Create a project
echo 3. Copy the DATABASE_URL from Neon console
echo 4. Update DATABASE_URL in all 3 .env files
echo 5. Test backend: cd backend ^& uv run uvicorn src.main:app --reload --port 8000
echo 6. Test frontend: cd frontend ^& npm run dev
echo.
pause

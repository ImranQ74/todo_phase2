@echo off
REM Setup script for Docker Compose - Windows Version
REM This script generates a secure random secret for JWT authentication

echo Setting up Docker Compose environment...
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file from .env.example
    exit /b 1
)

REM Generate a random secret using PowerShell or OpenSSL if available
echo Generating secure secret for JWT authentication...

REM Check if OpenSSL is available
where openssl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Using OpenSSL to generate secret...
    for /f %%i in ('openssl rand -base64 32') do set SECRET=%%i
) else (
    REM Fallback to PowerShell
    echo Using PowerShell to generate secret...
    for /f %%i in ('powershell -Command "[Convert]::ToBase64String([Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes(32))"
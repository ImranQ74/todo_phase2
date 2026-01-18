#!/usr/bin/env python3
"""Setup and Configuration Script for Todo Phase 2"""

import os
import secrets
import sys

def generate_secret():
    """Generate a secure 32-character JWT secret."""
    return secrets.token_urlsafe(32)

def update_env_file(filepath, secret):
    """Update .env file with generated secret."""
    try:
        # Read current content
        with open(filepath, 'r') as f:
            content = f.read()

        # Write updated content
        with open(filepath, 'w') as f:
            for line in content.split('\n'):
                if 'BETTER_AUTH_SECRET=' in line and 'your-256-bit-secret' in line:
                    f.write(f'BETTER_AUTH_SECRET={secret}\n')
                elif 'BETTER_AUTH_SECRET=' in line and 'your-generated-secret' in line:
                    f.write(f'BETTER_AUTH_SECRET={secret}\n')
                else:
                    f.write(f'{line}\n')

        print(f"      Updated {filepath}")
        return True
    except Exception as e:
        print(f"      ERROR updating {filepath}: {e}")
        return False

def check_file(filepath, description):
    """Check if file exists and report."""
    exists = os.path.exists(filepath)
    status = "OK" if exists else "MISSING"
    print(f"      {description}: {status}")
    return exists

def main():
    print("==========================================")
    print("TODO PHASE 2 - SETUP DIAGNOSTIC")
    print("==========================================")
    print()

    # Generate secret
    print("1. Generating secure JWT secret...")
    jwt_secret = generate_secret()
    print(f"   Generated: {jwt_secret[:30]}...")
    print()

    # Update root .env
    print("2. Updating environment files...")
    root_env = ".env"
    if os.path.exists(root_env):
        update_env_file(root_env, jwt_secret)
    else:
        print(f"   WARNING: {root_env} not found")
    print()

    # Update backend .env
    backend_env = "backend/.env"
    if os.path.exists(backend_env):
        update_env_file(backend_env, jwt_secret)
    else:
        print(f"   WARNING: {backend_env} not found")
    print()

    # Update frontend .env.local
    frontend_env = "frontend/.env.local"
    if os.path.exists(frontend_env):
        update_env_file(frontend_env, jwt_secret)
    else:
        print(f"   WARNING: {frontend_env} not found")
    print()

    # Check critical files
    print("3. Verifying project structure...")
    files_to_check = [
        ("backend/src/main.py", "Backend entry point"),
        ("backend/src/config.py", "Backend config"),
        ("backend/src/database.py", "Database module"),
        ("backend/src/routers/tasks.py", "API routes"),
        ("frontend/package.json", "Frontend package"),
        ("frontend/src/app/page.tsx", "Landing page"),
        ("frontend/src/app/signin/page.tsx", "Signin page"),
        ("frontend/src/app/signup/page.tsx", "Signup page"),
        ("frontend/src/app/dashboard/page.tsx", "Dashboard"),
    ]

    for filepath, desc in files_to_check:
        check_file(filepath, desc)
    print()

    # Summary
    print("==========================================")
    print("SETUP COMPLETE")
    print("==========================================")
    print()
    print("Summary:")
    print(f"  - Generated JWT secret: {len(jwt_secret)} chars")
    print(f"  - Updated .env files with new secret")
    print()
    print("NEXT STEPS:")
    print("  1. Get Neon database URL from https://console.neon.tech")
    print("  2. Update DATABASE_URL in all .env files")
    print("  3. Install backend deps: cd backend && uv sync")
    print("  4. Install frontend deps: cd frontend && npm install")
    print("  5. Test backend: cd backend && uv run uvicorn src.main:app --reload --port 8000")
    print("  6. Test frontend: cd frontend && npm run dev")
    print()

if __name__ == "__main__":
    main()

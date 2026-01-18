#!/usr/bin/env python3
"""Test if all backend dependencies are installed"""

print("="*60)
print("BACKEND DEPENDENCY TEST")
print("="*60)
print()

# Installation status
deps_status = {}

def check_import(module_name, import_name=None):
    """Check if a module can be imported."""
    try:
        if import_name is None:
            __import__(module_name)
        else:
            __import__(import_name)
        return "INSTALLED"
    except Exception as e:
        return f"FAILED: {e}"

# Core dependencies
core_deps = [
    ("fastapi", "FastAPI framework"),
    ("sqlmodel", "SQLModel ORM"),
    ("pydantic", "Pydantic models"),
    ("jose", "Python-JOSE (JWT)"),
    ("asyncpg", "AsyncPG (PostgreSQL)"),
    ("uvicorn", "Uvicorn server"),
    ("httpx", "HTTPX client"),
]

print("1. Core Dependencies:")
for module, desc in core_deps:
    status = check_import(module)
    print(f"   {desc}: {status}")
    deps_status[desc] = status
print()

# Configuration test
try:
    from src.config import get_settings
    settings = get_settings()
    print("2. Configuration Load: SUCCESS")
    print(f"   - Database URL configured: {'Yes' if settings.database_url else 'No'}")
    print(f"   - Auth secret length: {len(settings.better_auth_secret)} chars")
    print(f"   - Algorithm: {settings.better_auth_algorithm}")
except Exception as e:
    print(f"2. Configuration Load: FAILED - {e}")
print()

# JWT test
try:
    from src.utils.jwt import create_jwt, decode_jwt
    token = create_jwt("test-user-123")
    payload = decode_jwt(token)
    if payload.get('sub') == 'test-user-123':
        print("3. JWT Functionality: SUCCESS")
        print(f"   - Token generated: {token[:30]}...")
        print(f"   - Decoded correctly: sub={payload.get('sub')}")
    else:
        print("3. JWT Functionality: FAILED - Payload mismatch")
except Exception as e:
    print(f"3. JWT Functionality: FAILED - {e}")
print()

# Summary
total_deps = len(core_deps)
installed_deps = sum(1 for _, status in [(desc, deps_status[desc]) for desc in [cd[1] for cd in core_deps]] if 'INSTALLED' in deps_status[desc])

print("="*60)
print("SUMMARY")
print("="*60)
print(f"Dependencies installed: {installed_deps}/{total_deps}")

if installed_deps == total_deps:
    print("✓ All dependencies installed!")
    print("You can now start testing the backend.")
else:
    print("✗ Some dependencies missing.")
    print("Please complete the installation.")

#!/usr/bin/env python3
"""Quick test to verify all dependencies can be imported"""

print("Importing dependencies...")

# Test core imports
try:
    import fastapi
    print("✓ fastapi imported")
except Exception as e:
    print(f"✗ fastapi: {e}")

try:
    import sqlmodel
    print("✓ sqlmodel imported")
except Exception as e:
    print(f"✗ sqlmodel: {e}")

try:
    import pydantic
    print("✓ pydantic imported")
except Exception as e:
    print(f"✗ pydantic: {e}")

try:
    import pydantic_settings
    print("✓ pydantic_settings imported")
except Exception as e:
    print(f"✗ pydantic_settings: {e}")

try:
    import jose
    print("✓ python-jose imported")
except Exception as e:
    print(f"✗ python-jose: {e}")

try:
    import asyncpg
    print("✓ asyncpg imported")
except Exception as e:
    print(f"✗ asyncpg: {e}")

try:
    import uvicorn
    print("✓ uvicorn imported")
except Exception as e:
    print(f"✗ uvicorn: {e}")

try:
    import httpx
    print("✓ httpx imported")
except Exception as e:
    print(f"✗ httpx: {e}")

print("\nTest configuration...")
try:
    from src.config import get_settings
    s = get_settings()
    print("✓ Config loads")
    print(f"  - Secret set: {len(s.better_auth_secret) > 0}")
except Exception as e:
    print(f"✗ Config error: {e}")

print("\nTest JWT...")
try:
    from src.utils.jwt import create_jwt, decode_jwt
    token = create_jwt("test")
    payload = decode_jwt(token)
    print("✓ JWT works")
    print(f"  - Token: {token[:20]}...")
    print(f"  - Sub: {payload.get('sub')}")
except Exception as e:
    print(f"✗ JWT error: {e}")

"""JWT utility functions for token encoding and decoding."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt

from src.config import get_settings


def decode_jwt(token: str) -> Dict[str, Any]:
    """Decode and verify a JWT token.

    Args:
        token: The JWT token string to decode

    Returns:
        Dict[str, Any]: Decoded token payload if valid

    Raises:
        JWTError: If token is invalid or expired
    """
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.better_auth_algorithm],
        )
        return payload
    except JWTError as e:
        # Re-raise the JWTError instead of returning a dict with sub=None
        raise e


def create_jwt(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token for a user.

    Used primarily for testing purposes. In production, Better Auth
    generates tokens on the frontend.

    Args:
        user_id: The user ID to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        str: Encoded JWT token
    """
    settings = get_settings()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)

    to_encode = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
    }

    return jwt.encode(
        to_encode,
        settings.better_auth_secret,
        algorithm=settings.better_auth_algorithm,
    )

"""Pydantic schemas for authentication."""

from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """JWT token payload schema.

    Represents the decoded payload from a JWT token.

    Attributes:
        sub: Subject (user ID)
        exp: Expiration timestamp
        iat: Issued at timestamp
    """

    sub: str  # user_id
    exp: Optional[int] = None
    iat: Optional[int] = None


class TokenResponse(BaseModel):
    """Schema for token validation response.

    Attributes:
        valid: Whether the token is valid
        user_id: User ID if valid, None otherwise
    """

    valid: bool
    user_id: Optional[str] = None

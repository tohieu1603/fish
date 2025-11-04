"""Authentication schemas."""
from ninja import Schema
from typing import Optional


class LoginSchema(Schema):
    """Login request schema."""
    username: str
    password: str


class RegisterSchema(Schema):
    """Register request schema."""
    username: str
    password: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "sale"


class UserOutSchema(Schema):
    """User output schema."""
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    role: str
    phone: str
    is_active: bool
    avatar: Optional[str] = None


class TokenSchema(Schema):
    """JWT token response schema."""
    access_token: str
    token_type: str
    user: UserOutSchema


class ErrorResponse(Schema):
    """Error response schema."""
    detail: str

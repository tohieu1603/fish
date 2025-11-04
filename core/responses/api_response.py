"""Standard API response formats."""
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    errors: Optional[dict] = None

    @classmethod
    def success_response(cls, data: T = None, message: str = "Success"):
        """Create success response."""
        return cls(success=True, message=message, data=data)

    @classmethod
    def error_response(cls, message: str = "Error", errors: dict = None):
        """Create error response."""
        return cls(success=False, message=message, errors=errors)


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    code: Optional[str] = None

"""Activity schemas."""
from ninja import Schema
from datetime import datetime
from typing import Optional


class UserInfoSchema(Schema):
    """User info in activity."""
    id: int
    username: str
    full_name: str
    email: Optional[str] = None


class OrderActivitySchema(Schema):
    """Order activity schema."""
    id: int
    activity_type: str
    description: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    metadata: Optional[dict] = None
    user: Optional[UserInfoSchema] = None
    created_at: datetime

    @staticmethod
    def resolve_user(obj):
        """Resolve user info."""
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'full_name': obj.user.get_full_name() or obj.user.username,
                'email': obj.user.email
            }
        return None

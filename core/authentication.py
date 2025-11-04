"""JWT Authentication for Django Ninja."""
from typing import Optional
import jwt
from django.conf import settings
from django.http import HttpRequest
from ninja.security import HttpBearer
from apps.users.models.user import User


class JWTAuth(HttpBearer):
    """JWT authentication class for Django Ninja."""

    def authenticate(self, request: HttpRequest, token: str) -> Optional[User]:
        """
        Authenticate user based on JWT token.

        Args:
            request: Django HTTP request
            token: JWT token from Authorization header

        Returns:
            User object if token is valid, None otherwise
        """
        try:
            # Decode JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            # Get user ID from token
            user_id = payload.get('user_id')
            if not user_id:
                return None

            # Fetch user from database
            user = User.objects.get(id=user_id, is_active=True)

            # Attach user to request for Django compatibility
            request.user = user

            return user

        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid
            return None
        except User.DoesNotExist:
            # User not found or inactive
            return None
        except Exception:
            # Any other error
            return None

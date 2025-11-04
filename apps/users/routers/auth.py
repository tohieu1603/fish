"""Authentication router for login, register, logout."""
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from ninja import Router
from ninja.errors import HttpError
from typing import Optional
import jwt
from django.conf import settings
from apps.users.models.user import User
from apps.users.schemas.auth_schema import (
    LoginSchema,
    RegisterSchema,
    TokenSchema,
    UserOutSchema,
    ErrorResponse
)
from core.authentication import JWTAuth

auth_router = Router(tags=["Authentication"])


def create_token(user: User) -> str:
    """Create JWT token for user."""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


@auth_router.post("/register", response={201: TokenSchema, 400: ErrorResponse})
def register(request, payload: RegisterSchema):
    """Register a new user."""
    # Check if username already exists
    if User.objects.filter(username=payload.username).exists():
        return 400, {"detail": "Username đã tồn tại"}

    # Check if email already exists
    if payload.email and User.objects.filter(email=payload.email).exists():
        return 400, {"detail": "Email đã tồn tại"}

    # Create user
    try:
        user = User.objects.create_user(
            username=payload.username,
            email=payload.email or "",
            password=payload.password,
            first_name=payload.first_name or "",
            last_name=payload.last_name or "",
            phone=payload.phone or "",
            role=payload.role or "sale"
        )

        # Create token
        token = create_token(user)

        return 201, {
            "access_token": token,
            "token_type": "Bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.get_full_name() or user.username,
                "role": user.role,
                "phone": user.phone,
                "is_active": user.is_active,
                "avatar": user.avatar.url if user.avatar else None
            }
        }
    except Exception as e:
        return 400, {"detail": f"Không thể tạo user: {str(e)}"}


@auth_router.post("/login", response={200: TokenSchema, 401: ErrorResponse})
def login_user(request, payload: LoginSchema):
    """Login user and return JWT token. Can login with username or email."""
    # Try to find user by username or email
    user = None
    try:
        # First try username
        user = User.objects.get(username=payload.username)
        print(f"Found user by username: {user.username}")
    except User.DoesNotExist:
        # If not found, try email
        try:
            user = User.objects.get(email=payload.username)
            print(f"Found user by email: {user.username}")
        except User.DoesNotExist:
            print(f"User not found with username/email: {payload.username}")
            return 401, {"detail": "Tên đăng nhập hoặc mật khẩu không đúng"}

    # Check password
    if not user.check_password(payload.password):
        print(f"Password check failed for user: {user.username}")
        return 401, {"detail": "Tên đăng nhập hoặc mật khẩu không đúng"}

    print(f"Password check passed for user: {user.username}")

    if not user.is_active:
        return 401, {"detail": "Tài khoản đã bị vô hiệu hóa"}

    # Create token
    token = create_token(user)

    # Log user in (for session-based auth as backup)
    login(request, user)

    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.get_full_name() or user.username,
            "role": user.role,
            "phone": user.phone,
            "is_active": user.is_active,
            "avatar": user.avatar.url if user.avatar else None
        }
    }


@auth_router.post("/logout", response={200: dict})
def logout_user(request):
    """Logout current user."""
    logout(request)
    return {"message": "Đăng xuất thành công"}


@auth_router.get("/me", response={200: UserOutSchema, 401: ErrorResponse}, auth=JWTAuth())
def get_current_user(request):
    """Get current logged-in user."""
    user = request.auth
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.get_full_name() or user.username,
        "role": user.role,
        "phone": user.phone,
        "is_active": user.is_active,
        "avatar": user.avatar.url if user.avatar else None
    }


@auth_router.get("/users", response={200: list[UserOutSchema], 401: ErrorResponse}, auth=JWTAuth())
def get_users(request):
    """Get all active users for assignment."""
    users = User.objects.filter(is_active=True).order_by('username')
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.get_full_name() or user.username,
            "role": user.role,
            "phone": user.phone,
            "is_active": user.is_active,
            "avatar": user.avatar.url if user.avatar else None
        }
        for user in users
    ]

"""Formatting utilities."""
from datetime import datetime, timedelta
from typing import Optional


def format_currency(amount: float) -> str:
    """Format amount as Vietnamese currency."""
    return f"{amount:,.0f}đ"


def format_datetime_vn(dt: datetime) -> str:
    """Format datetime in Vietnamese format."""
    return dt.strftime("%d/%m/%Y %H:%M")


def format_date_vn(dt: datetime) -> str:
    """Format date in Vietnamese format."""
    return dt.strftime("%d/%m/%Y")


def calculate_deadline(created_at: datetime, duration_minutes: int) -> datetime:
    """Calculate deadline based on created time and duration."""
    return created_at + timedelta(minutes=duration_minutes)


def get_remaining_time(deadline: datetime, current_time: Optional[datetime] = None) -> timedelta:
    """Get remaining time until deadline."""
    if current_time is None:
        current_time = datetime.now()
    return deadline - current_time

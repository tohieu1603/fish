"""Common validators."""
import re
from typing import Optional


def validate_phone_number(phone: str) -> bool:
    """Validate Vietnamese phone number."""
    pattern = r'^(0|\+84)[1-9][0-9]{8}$'
    return bool(re.match(pattern, phone))


def validate_positive_number(value: float) -> bool:
    """Validate positive number."""
    return value > 0


def validate_non_negative_number(value: float) -> bool:
    """Validate non-negative number."""
    return value >= 0

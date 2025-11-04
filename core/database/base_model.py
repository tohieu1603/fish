"""Base model for all Django models."""
from django.db import models


class BaseModel(models.Model):
    """Abstract base model with common fields."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        abstract = True
        ordering = ['-created_at']

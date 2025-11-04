"""User model."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.enums.base_enum import UserRole


class User(AbstractUser):
    """Extended User model."""

    role = models.CharField(
        max_length=20,
        choices=[(role.value, UserRole.get_label(role)) for role in UserRole],
        default=UserRole.SALE.value,
        verbose_name='Vai trò'
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name='Số điện thoại')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Ảnh đại diện')

    class Meta:
        db_table = 'users'
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'

    def __str__(self):
        return self.get_full_name() or self.username

    # Fix reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )

"""Database mixins for common functionality."""
from django.db import models


class SoftDeleteMixin(models.Model):
    """Mixin for soft delete functionality."""

    is_deleted = models.BooleanField(default=False, verbose_name='Đã xóa')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày xóa')

    class Meta:
        abstract = True

    def soft_delete(self):
        """Soft delete the object."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class TimestampMixin(models.Model):
    """Mixin for timestamp fields."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')

    class Meta:
        abstract = True

"""Order activity tracking model."""
from django.db import models
from django.conf import settings


class OrderActivity(models.Model):
    """Track all activities and changes on orders."""

    ACTIVITY_TYPES = [
        ('status_change', 'Thay đổi trạng thái'),
        ('created', 'Tạo đơn hàng'),
        ('updated', 'Cập nhật thông tin'),
        ('image_uploaded', 'Upload ảnh'),
        ('image_deleted', 'Xóa ảnh'),
        ('comment', 'Thêm ghi chú'),
    ]

    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='Đơn hàng'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_activities',
        verbose_name='Người thực hiện'
    )
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES,
        verbose_name='Loại hoạt động'
    )
    description = models.TextField(
        verbose_name='Mô tả',
        help_text='Mô tả chi tiết hoạt động'
    )
    old_value = models.TextField(
        blank=True,
        null=True,
        verbose_name='Giá trị cũ'
    )
    new_value = models.TextField(
        blank=True,
        null=True,
        verbose_name='Giá trị mới'
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        verbose_name='Dữ liệu bổ sung',
        help_text='Dữ liệu JSON bổ sung về hoạt động'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Thời gian'
    )

    class Meta:
        db_table = 'order_activities'
        verbose_name = 'Lịch sử đơn hàng'
        verbose_name_plural = 'Lịch sử đơn hàng'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order', '-created_at']),
            models.Index(fields=['activity_type']),
        ]

    def __str__(self):
        return f"{self.order.order_number} - {self.get_activity_type_display()} - {self.created_at}"

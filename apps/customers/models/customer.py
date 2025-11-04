"""Customer model."""
from django.db import models
from core.database.base_model import BaseModel


class Customer(BaseModel):
    """Customer model."""

    name = models.CharField(max_length=255, verbose_name='Tên khách hàng')
    phone = models.CharField(max_length=15, verbose_name='Số điện thoại', unique=True)
    address = models.TextField(verbose_name='Địa chỉ')
    email = models.EmailField(blank=True, verbose_name='Email')
    notes = models.TextField(blank=True, verbose_name='Ghi chú')
    is_vip = models.BooleanField(default=False, verbose_name='Khách VIP')

    class Meta:
        db_table = 'customers'
        verbose_name = 'Khách hàng'
        verbose_name_plural = 'Khách hàng'
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - {self.phone}"

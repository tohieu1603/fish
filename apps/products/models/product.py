"""Product model."""
from django.db import models
from core.database.base_model import BaseModel


class Product(BaseModel):
    """Seafood product model."""

    name = models.CharField(max_length=255, verbose_name='Tên sản phẩm')
    unit = models.CharField(max_length=50, default='kg', verbose_name='Đơn vị')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Giá')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Hình ảnh')
    in_stock = models.BooleanField(default=True, verbose_name='Còn hàng')

    class Meta:
        db_table = 'products'
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.unit})"

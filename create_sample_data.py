import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.users.models import User
from core.enums.base_enum import OrderStatus
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

# Create products
products_data = [
    {"name": "Tôm hùm", "price": 1200000, "unit": "kg"},
    {"name": "Cua hoàng đế", "price": 800000, "unit": "kg"},
    {"name": "Ghẹ", "price": 250000, "unit": "kg"},
    {"name": "Mực ống", "price": 150000, "unit": "kg"},
    {"name": "Tôm sú", "price": 350000, "unit": "kg"},
]

print("Creating products...")
for data in products_data:
    Product.objects.get_or_create(
        name=data["name"], defaults={"price": data["price"], "unit": data["unit"]}
    )

products = list(Product.objects.all())
admin_user = User.objects.first()

# Create sample orders
print("Creating sample orders...")
orders_data = [
    {
        "customer_name": "Nguyễn Văn An",
        "customer_phone": "0901234567",
        "customer_address": "123 Lê Lợi, Quận 1, TP.HCM",
        "status": OrderStatus.CREATED,
        "items": [{"product": products[0], "quantity": 2}],
    },
    {
        "customer_name": "Trần Thị Bình",
        "customer_phone": "0912345678",
        "customer_address": "456 Nguyễn Huệ, Quận 1, TP.HCM",
        "status": OrderStatus.WEIGHING,
        "items": [
            {"product": products[1], "quantity": 1.5},
            {"product": products[3], "quantity": 1},
        ],
    },
    {
        "customer_name": "Lê Văn Cường",
        "customer_phone": "0923456789",
        "customer_address": "789 Pasteur, Quận 3, TP.HCM",
        "status": OrderStatus.PAYMENT,
        "items": [{"product": products[2], "quantity": 3}],
    },
]

for idx, order_data in enumerate(orders_data, 1):
    order = Order.objects.create(
        order_number=f"DH{str(idx).zfill(3)}",
        customer_name=order_data["customer_name"],
        customer_phone=order_data["customer_phone"],
        customer_address=order_data["customer_address"],
        status=order_data["status"],
        shipping_fee=30000,
        chip_fee=10000,
        created_by=admin_user,
        delivery_time=timezone.now() + timedelta(hours=3),
    )

    if admin_user:
        order.assigned_to.add(admin_user)

    for item_data in order_data["items"]:
        product = item_data["product"]
        quantity = Decimal(str(item_data["quantity"]))
        price = product.price

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            quantity=quantity,
            unit=product.unit,
            price=price,
        )

    order.calculate_total()

print(f"Created {len(orders_data)} sample orders successfully!")

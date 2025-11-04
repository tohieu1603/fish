"""Seed database with comprehensive sample data."""
import os
import django
import random
from datetime import timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from django.utils import timezone
from apps.orders.models import Order, OrderItem, OrderStatusHistory
from apps.products.models import Product
from apps.users.models import User
from core.enums.base_enum import OrderStatus, UserRole

print("=" * 60)
print("SEEDING DATABASE WITH SAMPLE DATA")
print("=" * 60)

# Clear existing data
print("\n[1/5] Clearing existing data...")
OrderItem.objects.all().delete()
OrderStatusHistory.objects.all().delete()
Order.objects.all().delete()
Product.objects.all().delete()
User.objects.filter(is_superuser=False).delete()

# Create users
print("\n[2/5] Creating users...")
users_data = [
    {
        "username": "admin",
        "password": "admin123",
        "email": "admin@seefood.com",
        "first_name": "Quản",
        "last_name": "Trị",
        "role": UserRole.ADMIN.value,
        "is_superuser": True,
        "is_staff": True,
    },
    {
        "username": "manager1",
        "password": "manager123",
        "email": "manager1@seefood.com",
        "first_name": "Nguyễn",
        "last_name": "Văn Minh",
        "role": UserRole.MANAGER.value,
    },
    {
        "username": "sale1",
        "password": "sale123",
        "email": "sale1@seefood.com",
        "first_name": "Trần",
        "last_name": "Thị Lan",
        "role": UserRole.SALE.value,
    },
    {
        "username": "sale2",
        "password": "sale123",
        "email": "sale2@seefood.com",
        "first_name": "Lê",
        "last_name": "Văn Hùng",
        "role": UserRole.SALE.value,
    },
    {
        "username": "kitchen1",
        "password": "kitchen123",
        "email": "kitchen1@seefood.com",
        "first_name": "Phạm",
        "last_name": "Văn Tâm",
        "role": UserRole.KITCHEN.value,
    },
    {
        "username": "kitchen2",
        "password": "kitchen123",
        "email": "kitchen2@seefood.com",
        "first_name": "Võ",
        "last_name": "Thị Mai",
        "role": UserRole.KITCHEN.value,
    },
]

created_users = {}
for user_data in users_data:
    password = user_data.pop("password")
    user, created = User.objects.get_or_create(
        username=user_data["username"],
        defaults=user_data
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"  ✓ Created user: {user.username} ({user.role})")
    else:
        print(f"  • User exists: {user.username} ({user.role})")
    created_users[user.username] = user

admin_user = created_users["admin"]

# Create products
print("\n[3/5] Creating products...")
products_data = [
    {"name": "Tôm hùm Alaska", "price": 1200000, "unit": "kg", "description": "Tôm hùm Alaska tươi sống"},
    {"name": "Cua hoàng đế", "price": 800000, "unit": "kg", "description": "Cua hoàng đế nhập khẩu"},
    {"name": "Ghẹ xanh", "price": 250000, "unit": "kg", "description": "Ghẹ xanh biển Cà Mau"},
    {"name": "Mực ống tươi", "price": 150000, "unit": "kg", "description": "Mực ống tươi sống"},
    {"name": "Tôm sú", "price": 350000, "unit": "kg", "description": "Tôm sú size lớn"},
    {"name": "Cá hồi Na Uy", "price": 450000, "unit": "kg", "description": "Cá hồi phi lê nhập khẩu"},
    {"name": "Bào ngư", "price": 1800000, "unit": "kg", "description": "Bào ngư tươi sống"},
    {"name": "Cá ngừ đại dương", "price": 320000, "unit": "kg", "description": "Cá ngừ vây vàng"},
    {"name": "Ốc hương", "price": 180000, "unit": "kg", "description": "Ốc hương biển miền Trung"},
    {"name": "Mực nang", "price": 200000, "unit": "kg", "description": "Mực nang tươi sống"},
]

products = []
for data in products_data:
    product, created = Product.objects.get_or_create(
        name=data["name"],
        defaults={
            "price": data["price"],
            "unit": data["unit"],
            "description": data.get("description", ""),
            "in_stock": True,
        }
    )
    products.append(product)
    if created:
        print(f"  ✓ Created product: {product.name} - {product.price:,}đ/{product.unit}")

# Create sample customers data
customers_data = [
    {"name": "Nguyễn Văn An", "phone": "0901234567", "address": "123 Lê Lợi, Quận 1, TP.HCM"},
    {"name": "Trần Thị Bình", "phone": "0912345678", "address": "456 Nguyễn Huệ, Quận 1, TP.HCM"},
    {"name": "Lê Văn Cường", "phone": "0923456789", "address": "789 Pasteur, Quận 3, TP.HCM"},
    {"name": "Phạm Thị Dung", "phone": "0934567890", "address": "321 Điện Biên Phủ, Quận Bình Thạnh, TP.HCM"},
    {"name": "Hoàng Văn E", "phone": "0945678901", "address": "147 Phan Xích Long, Q.Phú Nhuận, TP.HCM"},
    {"name": "Võ Thị F", "phone": "0956789012", "address": "258 Trần Hưng Đạo, Q.1, TP.HCM"},
    {"name": "Đỗ Văn G", "phone": "0967890123", "address": "951 Võ Văn Kiệt, Q.5, TP.HCM"},
    {"name": "Mai Thị H", "phone": "0978901234", "address": "753 Xô Viết Nghệ Tĩnh, Q.Bình Thạnh, TP.HCM"},
    {"name": "Bùi Văn I", "phone": "0989012345", "address": "159 Hai Bà Trưng, Q.3, TP.HCM"},
    {"name": "Tôn Thị K", "phone": "0990123456", "address": "357 Lý Thường Kiệt, Q.10, TP.HCM"},
]

# Create orders
print("\n[4/5] Creating sample orders...")

all_statuses = [
    OrderStatus.CREATED,
    OrderStatus.WEIGHING,
    OrderStatus.CREATE_INVOICE,
    OrderStatus.SEND_PHOTO,
    OrderStatus.PAYMENT,
    OrderStatus.IN_KITCHEN,
    OrderStatus.PROCESSING,
    OrderStatus.DELIVERY,
    OrderStatus.COMPLETED,
]

order_count = 0
for status in all_statuses:
    # Create 5-8 orders per status
    num_orders = random.randint(5, 8)

    for i in range(num_orders):
        customer = random.choice(customers_data)

        # Random number of items (1-4)
        num_items = random.randint(1, 4)
        selected_products = random.sample(products, num_items)

        # Calculate deadline based on status
        if status == OrderStatus.COMPLETED:
            created_at = timezone.now() - timedelta(days=random.randint(1, 7))
            deadline = created_at + timedelta(hours=random.randint(2, 8))
            delivery_time = created_at + timedelta(hours=random.randint(3, 10))
        else:
            created_at = timezone.now() - timedelta(hours=random.randint(1, 48))
            # Some orders should be overdue
            if random.random() < 0.3:  # 30% overdue
                deadline = timezone.now() - timedelta(minutes=random.randint(10, 120))
            else:
                deadline = timezone.now() + timedelta(minutes=random.randint(10, 180))
            delivery_time = None

        # Create order
        order = Order.objects.create(
            customer_name=customer["name"],
            customer_phone=customer["phone"],
            customer_address=customer["address"],
            status=status.value,
            status_changed_at=created_at,
            deadline=deadline,
            delivery_time=delivery_time,
            shipping_fee=Decimal("30000"),
            chip_fee=Decimal("10000"),
            created_by=random.choice(list(created_users.values())),
            created_at=created_at,
            updated_at=created_at,
        )

        # Assign random users
        assigned_users = random.sample(list(created_users.values()), random.randint(1, 3))
        order.assigned_to.set(assigned_users)

        # Create order items
        subtotal = Decimal("0")
        for product in selected_products:
            quantity = Decimal(str(random.uniform(0.5, 3.0))).quantize(Decimal("0.1"))
            price = product.price
            total = quantity * price
            subtotal += total

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                unit=product.unit,
                price=price,
            )

        # Update order total
        order.subtotal = subtotal
        order.total = subtotal + order.shipping_fee + order.chip_fee
        order.save()

        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            from_status=OrderStatus.CREATED.value if status != OrderStatus.CREATED else "",
            to_status=status.value,
            changed_by=random.choice(list(created_users.values())),
        )

        order_count += 1

print(f"  ✓ Created {order_count} orders across all statuses")

# Print summary
print("\n[5/5] Summary:")
print("-" * 60)
print(f"  Users:    {User.objects.count()}")
print(f"  Products: {Product.objects.count()}")
print(f"  Orders:   {Order.objects.count()}")
print(f"  Items:    {OrderItem.objects.count()}")
print("\nOrders by status:")
for status in all_statuses:
    count = Order.objects.filter(status=status.value).count()
    print(f"  • {status.value:15s}: {count:3d} orders")

print("\n" + "=" * 60)
print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nLogin credentials:")
print("  Admin:   username='admin'    password='admin123'")
print("  Manager: username='manager1' password='manager123'")
print("  Sale:    username='sale1'    password='sale123'")
print("  Kitchen: username='kitchen1' password='kitchen123'")
print("=" * 60)

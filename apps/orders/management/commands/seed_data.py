"""Seed data for users and orders."""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random

from apps.users.models import User
from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem
from core.enums.base_enum import UserRole, OrderStatus


class Command(BaseCommand):
    help = 'Seed database with sample users, customers, and orders'

    def handle(self, *args, **options):
        self.stdout.write('Starting seed data...')

        # 1. Create Users
        self.stdout.write('\n1. Creating users...')
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        # 2. Create Customers
        self.stdout.write('\n2. Creating customers...')
        customers = self.create_customers()
        self.stdout.write(self.style.SUCCESS(f'Created {len(customers)} customers'))

        # 3. Create Orders
        self.stdout.write('\n3. Creating orders...')
        orders = self.create_orders(users, customers)
        self.stdout.write(self.style.SUCCESS(f'Created {len(orders)} orders'))

        self.stdout.write(self.style.SUCCESS('\n✅ Seed data completed successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Manager: manager / manager123')
        self.stdout.write('  Sale: sale1 / sale123')
        self.stdout.write('  Weighing: weighing1 / weighing123')
        self.stdout.write('  Kitchen: kitchen1 / kitchen123')

    def create_users(self):
        """Create sample users with different roles."""
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@seafood.vn',
                'first_name': 'Quản trị',
                'last_name': 'Nguyễn',
                'role': UserRole.ADMIN.value,
                'phone': '0901234567',
                'password': 'admin123',
                'is_superuser': True,
                'is_staff': True,
            },
            {
                'username': 'manager',
                'email': 'manager@seafood.vn',
                'first_name': 'Quản lý',
                'last_name': 'Trần',
                'role': UserRole.MANAGER.value,
                'phone': '0902234567',
                'password': 'manager123',
                'is_staff': True,
            },
            {
                'username': 'sale1',
                'email': 'sale1@seafood.vn',
                'first_name': 'Bán hàng',
                'last_name': 'Lê',
                'role': UserRole.SALE.value,
                'phone': '0903234567',
                'password': 'sale123',
            },
            {
                'username': 'sale2',
                'email': 'sale2@seafood.vn',
                'first_name': 'Thu',
                'last_name': 'Phạm',
                'role': UserRole.SALE.value,
                'phone': '0904234567',
                'password': 'sale123',
            },
            {
                'username': 'weighing1',
                'email': 'weighing1@seafood.vn',
                'first_name': 'Cân hàng',
                'last_name': 'Hoàng',
                'role': UserRole.WEIGHING.value,
                'phone': '0905234567',
                'password': 'weighing123',
            },
            {
                'username': 'kitchen1',
                'email': 'kitchen1@seafood.vn',
                'first_name': 'Bếp',
                'last_name': 'Võ',
                'role': UserRole.KITCHEN.value,
                'phone': '0906234567',
                'password': 'kitchen123',
            },
        ]

        users = []
        for data in users_data:
            password = data.pop('password')
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults=data
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'  ✓ {user.username} ({UserRole.get_label(UserRole(user.role))})')
            users.append(user)

        return users


    def create_customers(self):
        """Create sample customers."""
        customers_data = [
            {
                'name': 'Nhà hàng Hải Sản Ngon',
                'phone': '0281234567',
                'address': '123 Lê Lợi, Q1, TP.HCM',
                'email': 'haisan@example.com',
                'is_vip': True,
                'notes': 'Khách hàng VIP, ưu tiên giao hàng'
            },
            {
                'name': 'Quán Ốc Minh',
                'phone': '0282234567',
                'address': '456 Nguyễn Trãi, Q5, TP.HCM',
                'email': 'ocminh@example.com',
                'is_vip': False,
            },
            {
                'name': 'Chợ Hải Sản Tươi',
                'phone': '0283234567',
                'address': '789 Võ Văn Tần, Q3, TP.HCM',
                'email': '',
                'is_vip': True,
            },
            {
                'name': 'Anh Tuấn',
                'phone': '0909123456',
                'address': '12 Điện Biên Phủ, Q10, TP.HCM',
                'email': 'tuan@example.com',
                'is_vip': False,
            },
            {
                'name': 'Chị Lan',
                'phone': '0908123456',
                'address': '34 Phan Xích Long, Phú Nhuận, TP.HCM',
                'email': '',
                'is_vip': False,
            },
        ]

        customers = []
        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                phone=data['phone'],
                defaults=data
            )
            if created:
                vip_mark = '⭐' if customer.is_vip else ''
                self.stdout.write(f'  ✓ {customer.name} {vip_mark}')
            customers.append(customer)

        return customers

    def create_orders(self, users, customers):
        """Create sample orders with different statuses across multiple days."""
        sale_users = [u for u in users if u.role == UserRole.SALE.value]
        admin_user = next(u for u in users if u.role == UserRole.ADMIN.value)

        # Danh sách sản phẩm hải sản để random
        seafood_items = [
            {'name': 'Ốc', 'unit': 'kg', 'price_range': (150000, 200000)},
            {'name': 'Tôm sú', 'unit': 'kg', 'price_range': (400000, 500000)},
            {'name': 'Cá hồi', 'unit': 'kg', 'price_range': (350000, 420000)},
            {'name': 'Mực ống', 'unit': 'kg', 'price_range': (250000, 300000)},
            {'name': 'Nghêu', 'unit': 'kg', 'price_range': (100000, 150000)},
            {'name': 'Cua', 'unit': 'kg', 'price_range': (350000, 450000)},
            {'name': 'Ghẹ', 'unit': 'kg', 'price_range': (300000, 400000)},
            {'name': 'Tôm hùm', 'unit': 'kg', 'price_range': (900000, 1000000)},
            {'name': 'Bạch tuộc', 'unit': 'kg', 'price_range': (200000, 280000)},
            {'name': 'Cá ngừ', 'unit': 'kg', 'price_range': (280000, 350000)},
            {'name': 'Sò điệp', 'unit': 'kg', 'price_range': (200000, 250000)},
            {'name': 'Hàu', 'unit': 'kg', 'price_range': (220000, 280000)},
        ]

        statuses = [
            OrderStatus.CREATED.value,
            OrderStatus.WEIGHING.value,
            OrderStatus.PAYMENT.value,
            OrderStatus.IN_KITCHEN.value,
            OrderStatus.PROCESSING.value,
            OrderStatus.DELIVERY.value,
            OrderStatus.COMPLETED.value,
        ]

        orders = []

        # Tạo đơn hàng cho 7 ngày gần đây
        for day_offset in range(6, -1, -1):  # Từ 6 ngày trước đến hôm nay
            # Mỗi ngày tạo 3-5 đơn
            num_orders = random.randint(3, 5)

            for i in range(num_orders):
                # Random customer và user
                customer = random.choice(customers)
                created_by = random.choice(sale_users)

                # Random status
                status = random.choice(statuses)

                # Tính thời gian
                base_time = timezone.now() - timedelta(days=day_offset)
                # Random giờ trong ngày (6h-20h)
                hour_offset = random.randint(-12, 12)
                created_at = base_time + timedelta(hours=hour_offset)
                delivery_time = created_at + timedelta(hours=random.randint(2, 6))

                # Tạo tên đơn
                order_name = f"Đơn {customer.name.split()[0]}"

                # Tạo đơn hàng
                order = Order.objects.create(
                    order_name=order_name,
                    customer_name=customer.name,
                    customer_phone=customer.phone,
                    customer_address=customer.address,
                    status=status,
                    delivery_time=delivery_time,
                    created_by=created_by,
                )
                order.created_at = created_at

                # Thêm 2-4 sản phẩm vào đơn
                num_items = random.randint(2, 4)
                selected_items = random.sample(seafood_items, num_items)

                subtotal = Decimal('0')
                for item in selected_items:
                    quantity = Decimal(str(random.uniform(1, 10))).quantize(Decimal('0.01'))
                    price = Decimal(random.randint(item['price_range'][0], item['price_range'][1]))
                    total = quantity * price

                    # Random note đôi khi
                    notes = ['', '', '', 'Size lớn', 'Tươi sống', 'Đã làm sạch']
                    note = random.choice(notes)

                    OrderItem.objects.create(
                        order=order,
                        product=None,  # Không liên kết Product
                        product_name=item['name'],
                        quantity=quantity,
                        unit=item['unit'],
                        price=price,
                        total=total,
                        note=note
                    )
                    subtotal += total

                # Cập nhật tổng tiền
                order.subtotal = subtotal
                order.shipping_fee = Decimal(random.choice([20000, 30000, 40000]))
                order.chip_fee = Decimal(random.choice([10000, 20000, 30000]))
                order.total = subtotal + order.shipping_fee + order.chip_fee
                order.save()

                orders.append(order)

                # Hiển thị ngày tạo
                created_date = created_at.strftime('%d/%m')
                self.stdout.write(
                    f'  ✓ [{created_date}] {order.order_name} - '
                    f'{OrderStatus.get_label(OrderStatus(order.status))} - '
                    f'{order.total:,.0f}đ'
                )

        return orders

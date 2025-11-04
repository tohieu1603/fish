import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.users.models import User


class Command(BaseCommand):
    help = 'Seed database with sample orders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of orders to create (default: 50)'
        )

    def handle(self, *args, **options):
        count = options['count']

        self.stdout.write(self.style.SUCCESS(f'Starting to seed {count} orders...'))

        # Danh sách tên khách hàng mẫu
        customer_names = [
            "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Thị D", "Hoàng Văn E",
            "Đặng Thị F", "Vũ Văn G", "Bùi Thị H", "Đỗ Văn I", "Ngô Thị K",
            "Dương Văn L", "Phan Thị M", "Trương Văn N", "Lý Thị O", "Võ Văn P",
            "Mai Thị Q", "Tô Văn R", "Chu Thị S", "Đinh Văn T", "Hồ Thị U"
        ]

        # Danh sách sản phẩm mẫu
        seafood_products = [
            {"name": "Ngao hoa", "unit": "kg", "price_range": (80000, 120000)},
            {"name": "Tôm hùm bông", "unit": "con", "price_range": (300000, 500000)},
            {"name": "Cá lăng", "unit": "kg", "price_range": (150000, 250000)},
            {"name": "Mực ống", "unit": "kg", "price_range": (200000, 350000)},
            {"name": "Cua hoàng đế", "unit": "con", "price_range": (400000, 600000)},
            {"name": "Sò điệp", "unit": "kg", "price_range": (100000, 180000)},
            {"name": "Cá hồi", "unit": "kg", "price_range": (250000, 400000)},
            {"name": "Nghêu", "unit": "kg", "price_range": (50000, 90000)},
            {"name": "Bào ngư", "unit": "con", "price_range": (500000, 800000)},
            {"name": "Tôm sú", "unit": "kg", "price_range": (180000, 280000)},
        ]

        # Danh sách trạng thái
        statuses = [
            'created', 'weighing', 'create_invoice', 'send_photo',
            'payment', 'in_kitchen', 'processing', 'delivery', 'completed'
        ]

        # Địa chỉ mẫu
        addresses = [
            "123 Nguyễn Huệ, Q.1, TP.HCM",
            "456 Lê Lợi, Q.3, TP.HCM",
            "789 Võ Văn Kiệt, Q.5, TP.HCM",
            "321 Điện Biên Phủ, Q.Bình Thạnh, TP.HCM",
            "654 Cách Mạng Tháng 8, Q.10, TP.HCM",
            "147 Phan Xích Long, Q.Phú Nhuận, TP.HCM",
            "258 Trần Hưng Đạo, Q.1, TP.HCM",
            "369 Hai Bà Trưng, Q.3, TP.HCM",
        ]

        # Get first user or create one
        try:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(
                    username='admin',
                    email='admin@seefood.com',
                    password='admin123',
                    role='admin'
                )
                self.stdout.write(self.style.SUCCESS('Created admin user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting user: {e}'))
            return

        created_count = 0

        for i in range(count):
            try:
                # Random data
                customer_name = random.choice(customer_names)
                customer_phone = f"09{random.randint(10000000, 99999999)}"
                customer_address = random.choice(addresses)
                status = random.choice(statuses)

                # Tạo thời gian ngẫu nhiên trong 7 ngày qua
                days_ago = random.randint(0, 7)
                hours_ago = random.randint(0, 23)
                created_time = timezone.now() - timedelta(days=days_ago, hours=hours_ago)

                # Tính deadline (thêm 2-4 giờ từ thời điểm tạo)
                deadline_hours = random.randint(2, 4)
                deadline = created_time + timedelta(hours=deadline_hours)

                # Tạo order
                order = Order.objects.create(
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    customer_address=customer_address,
                    status=status,
                    created_at=created_time,
                    deadline=deadline,
                    chip_fee=random.choice([0, 10000, 20000, 30000]),
                    shipping_fee=random.choice([15000, 20000, 25000, 30000]),
                    notes=f"Đơn hàng mẫu số {i+1}",
                    created_by=user
                )

                # Thêm assigned user
                order.assigned_to.add(user)

                # Tạo 2-5 order items
                num_items = random.randint(2, 5)
                total = 0

                for _ in range(num_items):
                    product_data = random.choice(seafood_products)
                    quantity = random.uniform(0.5, 3.0)  # 0.5kg đến 3kg
                    price = random.randint(product_data['price_range'][0], product_data['price_range'][1])

                    # Tạo hoặc lấy product
                    product, _ = Product.objects.get_or_create(
                        name=product_data['name'],
                        defaults={
                            'description': f"Sản phẩm hải sản tươi sống - {product_data['name']}",
                            'unit': product_data['unit'],
                            'price': price
                        }
                    )

                    # Tạo order item
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product_data['name'],
                        quantity=round(quantity, 1),
                        unit=product_data['unit'],
                        price=price
                    )

                    total += quantity * price

                # Update total
                order.total = total + order.chip_fee + order.shipping_fee
                order.save()

                created_count += 1

                if (created_count) % 10 == 0:
                    self.stdout.write(self.style.SUCCESS(f'Created {created_count} orders...'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating order {i+1}: {e}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} orders!'))
        self.stdout.write(self.style.SUCCESS('You can now view them in the frontend.'))

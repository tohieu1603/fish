"""Base enum class for all enums."""
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enum matching 10-step process."""

    CREATED = "created"  # 1. Tạo đơn
    WEIGHING = "weighing"  # 2. Cân hàng
    CREATE_INVOICE = "create_invoice"  # 3. Tạo phiếu ĐH
    SEND_PHOTO = "send_photo"  # 4. Gửi ảnh cân
    PAYMENT = "payment"  # 5. Thanh toán
    IN_KITCHEN = "in_kitchen"  # 6. Vào bếp
    PROCESSING = "processing"  # 7. Chế biến
    DELIVERY = "delivery"  # 8. Giao hàng
    COMPLETED = "completed"  # 9. Hoàn thành
    FAILED = "failed"  # 10. Thất bại

    @classmethod
    def get_label(cls, status):
        """Get Vietnamese label for status."""
        labels = {
            cls.CREATED: "Tạo đơn",
            cls.WEIGHING: "Cân hàng",
            cls.CREATE_INVOICE: "Tạo phiếu ĐH",
            cls.SEND_PHOTO: "Gửi ảnh cân",
            cls.PAYMENT: "Thanh toán",
            cls.IN_KITCHEN: "Vào bếp",
            cls.PROCESSING: "Chế biến",
            cls.DELIVERY: "Giao hàng",
            cls.COMPLETED: "Hoàn thành",
            cls.FAILED: "Thất bại",
        }
        return labels.get(status, status)

    @classmethod
    def get_duration_minutes(cls, status):
        """Get standard duration in minutes for each status."""
        durations = {
            cls.CREATED: 15,
            cls.WEIGHING: 20,
            cls.CREATE_INVOICE: 10,
            cls.SEND_PHOTO: 10,
            cls.PAYMENT: 30,
            cls.IN_KITCHEN: 60,
            cls.PROCESSING: 45,
            cls.DELIVERY: 30,
            cls.COMPLETED: 0,
            cls.FAILED: 0,
        }
        return durations.get(status, 0)


class UserRole(str, Enum):
    """User role enum."""

    ADMIN = "admin"
    MANAGER = "manager"
    SALE = "sale"
    WEIGHING = "weighing"
    KITCHEN = "kitchen"

    @classmethod
    def get_label(cls, role):
        """Get Vietnamese label for role."""
        labels = {
            cls.ADMIN: "Quản trị viên",
            cls.MANAGER: "Quản lý",
            cls.SALE: "Nhân viên bán hàng",
            cls.WEIGHING: "Bộ phận cân hàng",
            cls.KITCHEN: "Bộ phận bếp",
        }
        return labels.get(role, role)

    @classmethod
    def get_allowed_statuses(cls, role):
        """Get allowed statuses for each role."""
        # Admin và Manager có thể làm tất cả
        if role in [cls.ADMIN, cls.MANAGER]:
            return [
                OrderStatus.CREATED,
                OrderStatus.WEIGHING,
                OrderStatus.CREATE_INVOICE,
                OrderStatus.SEND_PHOTO,
                OrderStatus.PAYMENT,
                OrderStatus.IN_KITCHEN,
                OrderStatus.PROCESSING,
                OrderStatus.DELIVERY,
                OrderStatus.COMPLETED,
                OrderStatus.FAILED,
            ]

        # Sale chỉ tạo đơn và làm các giai đoạn đầu (đến thanh toán)
        if role == cls.SALE:
            return [
                OrderStatus.CREATED,
                OrderStatus.WEIGHING,
                OrderStatus.CREATE_INVOICE,
                OrderStatus.SEND_PHOTO,
                OrderStatus.PAYMENT,
            ]

        # Cân hàng chỉ làm giai đoạn cân
        if role == cls.WEIGHING:
            return [
                OrderStatus.WEIGHING,
                OrderStatus.CREATE_INVOICE,
                OrderStatus.SEND_PHOTO,
            ]

        # Bếp chỉ làm giai đoạn bếp (vào bếp -> chế biến -> giao hàng -> hoàn thành)
        if role == cls.KITCHEN:
            return [
                OrderStatus.IN_KITCHEN,
                OrderStatus.PROCESSING,
                OrderStatus.DELIVERY,
                OrderStatus.COMPLETED,
            ]

        return []

    @classmethod
    def can_transition(cls, role, from_status, to_status):
        """Check if role can transition from one status to another."""
        allowed_statuses = cls.get_allowed_statuses(role)

        # Admin và Manager có thể chuyển bất kỳ trạng thái nào
        if role in [cls.ADMIN, cls.MANAGER]:
            return True

        # Check if both statuses are in allowed list
        return from_status in allowed_statuses and to_status in allowed_statuses

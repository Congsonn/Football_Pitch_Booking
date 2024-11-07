from django.db import models


class PitchSize(models.TextChoices):
    _20mx40m = "20mx40m", "20m x 40m"
    _30mx50m = "30mx50m", "30m x 50m"
    _30mx60m = "30mx60m", "30m x 60m"
    _68mx105m = "68mx105m", "68m x 105m"


class PitchStatus(models.TextChoices):
    AVAILABLE = "available", "Có sẵn"
    UNAVAILABLE = "unavailable", "Không có sẵn"
    MAINTENANCE = "maintenance", "Bảo trì"


class BookingStatus(models.TextChoices):
    BOOKED = "booked", "Đã đặt"
    CANCELED = "canceled", "Đã hủy"
    PAID = "paid", "Đã thanh toán"


class PaymentMethod(models.TextChoices):
    CASH = "cash", "Tiền mặt"
    BANK_TRANSFER = "bank_transfer", "Chuyển khoản"
    CREDIT_CARD = "credit_card", "Thẻ tín dụng"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Chờ thành toán"
    COMPLETED = "completed", "Thanh toán thành công"
    FAILED = "failed", "Hủy thanh toán"
    REFUNDED = "refunded", "Hoàn tiền"

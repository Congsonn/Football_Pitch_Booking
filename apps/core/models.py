from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField

from .utils import format_number_with_commas
from .enums import PitchSize, PitchStatus, BookingStatus, PaymentMethod, PaymentStatus

User = get_user_model()
# Create your models here.
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Pitch(TimestampedModel):
    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="PIT")
    name = models.CharField(max_length=100,verbose_name="Tên sân")
    image = models.ImageField(
        upload_to="images/pitches/",
        default="default/noimage.jpg",
    )
    image_1 = models.ImageField(upload_to="images/pitches/", blank=True)
    image_2 = models.ImageField(upload_to="images/pitches/", blank=True)
    location = models.CharField(max_length=255, verbose_name="Địa điểm")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá mỗi giờ")
    size = models.CharField(
        max_length=8,
        choices=PitchSize.choices,
        verbose_name="Kích thước",
    )

    class Meta:
        verbose_name_plural = "Sân bóng"
        verbose_name = "Sân bóng"

    def __str__(self):
        return self.name
    

class Booking(TimestampedModel):
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Người đặt")

    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="BOO")
    booking_date = models.DateField(verbose_name="Ngày đặt")
    start_time = models.TimeField(verbose_name="Giờ bắt đầu")
    end_time = models.TimeField(verbose_name="Giờ kết thúc")
    messsage = models.TextField(blank=True)
    status = models.CharField(
        max_length=8,
        choices=BookingStatus.choices,
        default=BookingStatus.BOOKED,
        verbose_name="Trạng thái"
    )

    class Meta:
        ordering = ["booking_date","start_time"]
        verbose_name_plural = "Đơn đặt sân"
        verbose_name = "Đơn đặt sân"

    def __str__(self):
        return self.pitch.name
    
    def get_datetime_booking(self):
        datetime = f"{self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")}, {self.booking_date.strftime("%d-%m-%Y")}"
        return datetime
    
    def get_total_booking_hours(self):
        time_delta = timedelta(
            hours=self.end_time.hour - self.start_time.hour,
            minutes=self.end_time.minute - self.start_time.minute
        )
        total_hours = time_delta.total_seconds() / 3600  # Convert seconds to hours
        return round(total_hours, 2)
    
    def get_total_amount(self):
        total_hours = Decimal(self.get_total_booking_hours())
        total_amount = total_hours * self.pitch.price_per_hour
        return round(total_amount, 2)  


class Payment(TimestampedModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    uuid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="PAY")
    amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Tổng tiền")
    payment_date = models.DateField(null=True,blank=True,verbose_name="Ngày thanh toán")
    payment_method = models.CharField(
        max_length=13,
        choices=PaymentMethod.choices,
        verbose_name="Phương thức thanh toán"
    )
    status = models.CharField(
        max_length=9,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="Trạng thái"
    )

    class Meta:
        verbose_name_plural = "Lịch sử thanh toán"
        verbose_name = "Lịch sử thanh toán"

    def __str__(self):
        return f"Thanh toán {format_number_with_commas(self.amount)}đ cho đơn {self.booking.uuid}"

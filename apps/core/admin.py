from django.contrib import admin
from django.utils.html import format_html

from .utils import format_number_with_commas
from .models import Pitch, Booking, Payment


# Register your models here.
class PitchAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "__str__",
        "size",
        "location",
        "price_per_hour_tag",
    )
    list_filter = ("name", "location", "size")
    search_fields = ("name", "location")
    ordering = ("name",)

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height:50px;" />'.format(
                    obj.image.url
                )
            )
        return "-"

    image_tag.short_description = "Ảnh sân"

    def price_per_hour_tag(self, obj):
        return f"{format_number_with_commas(obj.price_per_hour)} đ"

    price_per_hour_tag.short_description = "Giá mỗi giờ"


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "user",
        "status",
        "booking_date",
        "start_time",
        "end_time",
    )
    list_filter = ("pitch__name", "status", "booking_date")
    search_fields = ("pitch__name", "uuid")
    ordering = ("booking_date", "start_time")


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "payment_method",
        "amount_tag",
        "status",
        "payment_date",
    )
    list_filter = (
        "booking__pitch__name",
        "booking__user",
        "payment_method",
        "status",
        "payment_date",
    )
    search_fields = ("booking__pitch__name", "booking__user", "payment_method")
    ordering = ["-created_at"]

    def amount_tag(self, obj):
        return f"{format_number_with_commas(obj.amount)} đ"

    amount_tag.short_description = "Tổng tiền"


admin.site.register(Pitch, PitchAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)

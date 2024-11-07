from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div

from apps.account.utils import submit_btn, indicator_elm, delete_btn
from .filters import get_available_pitches
from .models import Booking, Payment
from .enums import BookingStatus


class BookingPitchForm(forms.ModelForm):
    booking_date = forms.DateField(
        label="Ngày đặt",
        input_formats=["%d-%m-%Y"],
        widget=forms.DateInput(),
    )

    class Meta:
        model = Booking
        fields = ["booking_date", "start_time", "end_time"]

    def __init__(self, pitch_instance=None, *args, **kwargs):
        self.pitch_instance = pitch_instance
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "p-4 !pt-0 md:p-5 space-y-4"

        self.helper.attrs = {
            "hx-target": "#booking-pitch-modal-body",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #booking_pitch_submit",
        }

        if pitch_instance:
            self.helper.attrs["hx-post"] = reverse(
                "htmx_booking_pitch",
                args=[pitch_instance.uuid],
            )

        self.helper.layout = Layout(
            Field(
                "start_time",
                template="crispy_form/timepicker.html",
            ),
            Field(
                "end_time",
                template="crispy_form/timepicker.html",
            ),
            Field(
                "booking_date",
                template="crispy_form/datepicker.html",
            ),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("booking_pitch_submit", "Đặt sân", False)),
                css_class="flex items-center justify-end",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get("booking_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if not self.pitch_instance:
            raise ValidationError("Không có thông tin sân đã chọn.")

        available_pitches = get_available_pitches(booking_date, start_time, end_time)

        if self.pitch_instance not in available_pitches:
            raise ValidationError("Sân đã chọn không khả dụng vào thời gian này.")

        return cleaned_data


class UpdateBookingPitchForm(BookingPitchForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        is_cancelable = False
        super().__init__(pitch_instance=None, *args, **kwargs)

        self.helper.attrs = {
            "oninput": "enableButton('update_booking_pitch_submit');",
            "hx-target": "#update-booking-pitch-modal-body",
            "hx-swap": "outerHTML",
            "hx-disabled-elt": "find #update_booking_pitch_submit",
        }

        if instance:
            delete_url = reverse(
                "htmx_cancel_booking",
                args=[instance.uuid],
            )
            is_cancelable = instance.status == BookingStatus.BOOKED
            self.helper.attrs["hx-post"] = reverse(
                "htmx_update_booking",
                args=[instance.uuid],
            )

        self.helper.layout = Layout(
            Field(
                "start_time",
                template="crispy_form/timepicker.html",
            ),
            Field(
                "end_time",
                template="crispy_form/timepicker.html",
            ),
            Field(
                "booking_date",
                template="crispy_form/datepicker.html",
            ),
            Div(
                HTML(indicator_elm()),
                (
                    HTML(
                        delete_btn(
                            "cancel_booking_btn",
                            delete_url,
                            label="Hủy đặt",
                            confirm_msg="Bạn có chắc chắn muốn hủy đặt sân này?",
                            modal_close_id="update-booking-pitch-modal",
                        )
                    )
                    if is_cancelable
                    else None
                ),
                HTML(submit_btn("update_booking_pitch_submit")),
                css_class="flex gap-3 items-center justify-end",
            ),
        )


class CreatePayment(forms.ModelForm):
    message = forms.CharField(
        max_length=255,
        required=False,
        label="Lời nhắn",
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    class Meta:
        model = Payment
        fields = ["booking", "amount", "payment_method"]

    def __init__(self, booking_instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = reverse("payment")
        self.helper.form_class = "space-y-4"

        if booking_instance:
            self.fields["amount"].initial = booking_instance.get_total_amount()
            self.fields["booking"].initial = booking_instance.id

        self.helper.layout = Layout(
            Field("amount", wrapper_class="hidden"),
            Field("booking", wrapper_class="hidden"),
            Field("payment_method"),
            Field("message"),
            Div(
                HTML(indicator_elm()),
                HTML(submit_btn("create_payment_submit", "Thanh toán", False)),
                css_class="flex items-center justify-end",
            ),
        )

import django_filters, json

from datetime import datetime, date
from django.db.models import Q
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

from .enums import PitchSize, BookingStatus
from .models import Pitch, Booking


def get_available_pitches(raw_date, start_time, end_time):
    conflicting_bookings = []
    date_obj = None

    try:
        if raw_date:
            if isinstance(raw_date, str):
                date_obj = datetime.strptime(raw_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            else:
                date_obj = raw_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    if date_obj is None or start_time is None or end_time is None:
        conflicting_bookings = []
    else:
        conflicting_bookings = Booking.objects.filter(
            Q(start_time__lt=end_time, end_time__gt=start_time),
            booking_date__gte=date_obj,
            # status=BookingStatus.PAID
        ).values_list("pitch__uuid", flat=True)

    available_pitches = Pitch.objects.exclude(uuid__in=conflicting_bookings)

    return available_pitches


class PitchFilter(django_filters.FilterSet):
    # l = django_filters.CharFilter(
    #     field_name="location",
    #     lookup_expr="icontaints",
    #     label="Địa điểm",
    # )

    s = django_filters.ChoiceFilter(
        choices=PitchSize.choices,
        field_name="size",
        lookup_expr="exact",
        label="Kích thước",
    )

    d = django_filters.DateFilter(label="Ngày đặt", input_formats=["%d-%m-%Y"])

    st = django_filters.TimeFilter(label="Giờ bắt đầu")

    et = django_filters.TimeFilter(label="Giờ kết thúc")

    class Meta:
        model = Pitch
        fields = ["s"]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)

        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
        self.form.helper.form_action = reverse("pitches")
        self.form.helper.form_class = "flex items-end gap-4 w-full"

        self.form.helper.layout = Layout(
            # Field("l", wrapper_class="w-full"),
            Field("s", wrapper_class="!mb-0 w-1/3"),
            Field(
                "d",
                wrapper_class="w-1/3 mb-3",
                template="crispy_form/datepicker.html",
                data_options=json.dumps(
                    {
                        "orientation": "bottom",
                    }
                ),
            ),
            Field(
                "st",
                wrapper_class="w-1/3 mb-3",
                template="crispy_form/timepicker.html",
            ),
            Field(
                "et",
                wrapper_class="w-1/3 mb-3",
                template="crispy_form/timepicker.html",
            ),
            HTML(
                """
                <input type="submit" value="Tìm kiếm" class="w-fit mb-3 h-[42px] cursor-pointer text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
                >
            """
            ),
        )

    def filter_queryset(self, queryset):
        original_data = self.data.copy()

        self.form.cleaned_data.pop("d", None)
        self.form.cleaned_data.pop("st", None)
        self.form.cleaned_data.pop("et", None)

        filtered_queryset = super().filter_queryset(queryset)
        self.form.cleaned_data = original_data

        return filtered_queryset

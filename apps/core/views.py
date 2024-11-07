import json
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Pitch, Booking, Payment
from .filters import PitchFilter
from .filters import get_available_pitches
from .forms import UpdateBookingPitchForm, CreatePayment
from .enums import PaymentMethod, PaymentStatus, BookingStatus


# Create your views here.
def home(request):
    pitch_filter = PitchFilter(request.GET, queryset=Pitch.objects.all())

    context = {
        "form": pitch_filter.form,
    }

    return render(request, "core/home.html", context)


def pitches(request):
    querystring = request.GET.copy()
    raw_date = querystring.get("d")
    start_time = querystring.get("st")
    end_time = querystring.get("et")

    available_pitches = get_available_pitches(raw_date, start_time, end_time)
    pitch_filter = PitchFilter(querystring, queryset=available_pitches)
    pitch_filter.form.helper.form_class = (
        "flex items-end gap-4 w-full flex-wrap lg:flex-nowrap"
    )

    context = {
        "form": pitch_filter.form,
        "pitches": pitch_filter.qs,
    }

    return render(request, "core/pitch.html", context)


def pitch(request, uuid):
    pitch = get_object_or_404(Pitch, uuid=uuid)
    bookings = Booking.objects.filter(
        pitch=pitch, booking_date__gte=date.today()
    ).select_related("user")

    user_bookings = bookings.filter(user=request.user)
    other_bookings = bookings.exclude(user=request.user)

    context = {
        "pitch": pitch,
        "user_bookings": user_bookings,
        "other_bookings": other_bookings,
    }

    return render(request, "core/pitch_detail.html", context)


@login_required
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)

    context = {
        "user_bookings": user_bookings,
    }
    return render(request, "core/bookings.html", context)


@login_required
def booking(request, uuid):
    booking = get_object_or_404(Booking, uuid=uuid, user=request.user)

    form = UpdateBookingPitchForm(instance=booking)
    create_payment_form = CreatePayment(booking_instance=booking)

    context = {
        "form": form,
        "create_payment_form": create_payment_form,
        "booking": booking,
    }
    return render(request, "core/booking.html", context)


@login_required
def payment(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        payment_method = post_data.get("payment_method")
        booking_id = post_data.get("booking")
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        pending_payments = Payment.objects.filter(
            booking=booking, status=PaymentStatus.PENDING
        )

        if pending_payments.count() > 0:
            pending_payments.delete()

        form = CreatePayment(data=request.POST)
        if form.is_valid() and booking.status != BookingStatus.PAID:
            new_payment = form.save(commit=False)
            if payment_method == PaymentMethod.CASH:
                new_payment.payment_date = date.today()
                new_payment.status = PaymentStatus.COMPLETED
                booking.status = BookingStatus.PAID
                booking.save()
            new_payment.save()

        context = {
            "form": form,
        }
        return render(request, "core/payment.html", context)

    return Http404()


def about_us(request):

    return render(request, "core/about_us.html")

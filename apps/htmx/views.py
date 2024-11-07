import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, resolve_url
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http.response import HttpResponse

from apps.account.forms import (
    ChangePasswordFormCustom,
    UpdateUserInfoForm,
    UpdateUserContact,
    UpdateUserAvatar,
    AddUserAddress,
    UpdateUserAddress,
    UserAddress,
)


# Create your views here.
def change_password(request):

    if request.method == "POST":
        form = ChangePasswordFormCustom(request.user, request.POST)
        hx_trigger = None

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Đổi mật khẩu thành công.")
            hx_trigger = {
                "updateModals": {
                    "close": ["change-password-modal"],
                }
            }

        ctx = {"form": form}
        response = render(request, "htmx/change_password.html", ctx)
        if hx_trigger:
            response["HX-Trigger"] = json.dumps(hx_trigger)
        return response

    return HttpResponse(status=204)


def update_info(request):
    if request.method == "POST":
        form = UpdateUserInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công.")

        ctx = {"form": form}
        return render(request, "htmx/update_info.html", ctx)

    return HttpResponse(status=204)


def update_contact(request):
    if request.method == "POST":
        form = UpdateUserContact(request.POST, instance=request.user)
        hx_trigger = None

        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin liên hệ thành công.")
            hx_trigger = {
                "updateModals": {
                    "close": ["update-contact-modal"],
                }
            }

        ctx = {"form": form}
        response = render(request, "htmx/update_contact.html", ctx)
        if hx_trigger:
            response["HX-Trigger"] = json.dumps(hx_trigger)
        return response

    return HttpResponse(status=204)


def update_avatar(request):
    if request.method == "POST":
        form = UpdateUserAvatar(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật avatar thành công.")

        ctx = {"form": form}
        response = render(request, "htmx/update_avatar.html", ctx)
        response["HX-Trigger"] = json.dumps(
            {
                "updateModals": {
                    "close": ["update-avatar-modal"],
                }
            }
        )
        return response

    return HttpResponse(status=204)


def add_address(request):
    if request.method == "POST":
        form_add = AddUserAddress(request.POST)
        user_address = UserAddress.objects.filter(user=request.user)

        if form_add.is_valid():
            address = form_add.save(commit=False)
            address.user = request.user
            address.save()

            form_add = AddUserAddress()
            messages.success(request, "Thêm địa chỉ thành công.")

        ctx = {
            "type": "add",
            "form_add": form_add,
            "user_address": user_address,
        }
        return render(request, "htmx/update_address.html", ctx)

    return HttpResponse(status=204)


def update_address(request, id):
    address = get_object_or_404(UserAddress, id=id)
    form_update = UpdateUserAddress(instance=address)

    if request.method == "POST":
        form_update = UpdateUserAddress(
            request.POST,
            instance=address,
        )
        user_address = UserAddress.objects.filter(user=request.user)

        if form_update.is_valid():
            form_update.save()

            form_add = AddUserAddress()
            messages.success(request, "Cập nhật địa chỉ thành công.")
            ctx = {
                "type": "update",
                "form_update": form_update,
                "form_add": form_add,
                "user_address": user_address,
            }
            response = render(request, "htmx/update_address.html", ctx)
            response["HX-Trigger"] = json.dumps(
                {
                    "updateModals": {
                        "close": ["update-address-modal"],
                    }
                }
            )
            return response
        else:
            return HttpResponse(status=204)

    ctx = {"form_update": form_update}
    return render(request, "htmx/update_address_form.html", ctx)


def delete_address(request, id):
    address = get_object_or_404(UserAddress, id=id)
    address.delete()
    messages.success(request, "Xóa địa chỉ thành công.")

    form_add = AddUserAddress()
    user_address = UserAddress.objects.filter(user=request.user)

    ctx = {
        "type": "delete",
        "form_add": form_add,
        "user_address": user_address,
    }

    response = render(request, "htmx/update_address.html", ctx)
    response["HX-Trigger"] = json.dumps(
        {
            "updateModals": {
                "close": ["update-address-modal"],
            }
        }
    )
    return response


# CORE
from apps.core.models import Pitch
from apps.core.models import Booking
from apps.core.forms import BookingPitchForm, UpdateBookingPitchForm


def booking_pitch(request, uuid):
    pitch = get_object_or_404(Pitch, uuid=uuid)
    form = BookingPitchForm(pitch_instance=pitch)

    if request.method == "POST":
        form = BookingPitchForm(data=request.POST, pitch_instance=pitch)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.pitch = pitch
            booking.user = request.user
            booking.save()
            # messages.success(request, "Đặt sân thành công.")
            return HttpResponse(
                status=204,
                headers={"HX-Redirect": resolve_url("booking", booking.uuid)},
            )

    context = {
        "form": form,
    }
    return render(request, "htmx/booking_pitch.html", context)


@login_required
def update_booking(request, uuid):
    if request.method == "POST":
        booking = get_object_or_404(Booking, uuid=uuid, user=request.user)
        form = UpdateBookingPitchForm(data=request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật đơn đặt sân thành công.")
        context = {
            "form": form,
        }
        return render(request, "htmx/update_booking_pitch.html", context)

    return HttpResponse(status=204)


@login_required
def cancel_booking(request, uuid):
    booking = get_object_or_404(Booking, uuid=uuid, user=request.user)
    booking.delete()
    messages.success(request, "Xóa địa chỉ thành công.")

    return HttpResponse(
        status=204,
        headers={"HX-Redirect": resolve_url("pitch", booking.pitch.uuid)},
    )

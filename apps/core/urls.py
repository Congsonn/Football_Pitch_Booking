from django.urls import path
from apps.core import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pitches", views.pitches, name="pitches"),
    path("pitches/<str:uuid>", views.pitch, name="pitch"),
    path("bookings", views.bookings, name="bookings"),
    path("bookings/<str:uuid>", views.booking, name="booking"),
    path("payment", views.payment, name="payment"),
    path("about_us", views.about_us, name="about_us"),
]

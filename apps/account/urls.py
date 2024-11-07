from django.urls import path, include
from apps.account import views

urlpatterns = [
    path("", views.profile_manager, name="profile_manager"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("sign_out", views.sign_out, name="sign_out"),
    path("delete_account", views.delete_account, name="delete_account"),
]

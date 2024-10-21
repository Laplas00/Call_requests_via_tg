from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name='login_page'),
    path("telegram-login/", views.login_view, name='login_view'),
    path("authenticate_telegram_user_by_params/", views.login_authentication, name='login_auth'),
]
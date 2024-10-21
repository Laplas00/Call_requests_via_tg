from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name='login_page'),
    path("telegram-login/", views.login_view, name='login_view'),
]
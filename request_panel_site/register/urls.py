from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name='login_page'),
    path("authenticate_login/", views.login_authentication, name='login_auth'),
]
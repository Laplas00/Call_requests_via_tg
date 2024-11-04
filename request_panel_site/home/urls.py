from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_panel, name='main_panel'),
    path('/get_requests', views.request_loader, name='request_loader'),
    path('/logout', views.logout, name='logout'),
] 
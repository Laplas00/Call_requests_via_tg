from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_panel, name='main_panel'),
] 
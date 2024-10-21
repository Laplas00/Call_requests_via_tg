from django.contrib import admin
from django.contrib.auth import logout
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from register import views

urlpatterns = [
    path("", include("register.urls")),
    path("", include("home.urls")),
    path('admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from django.urls import path
from django.views import debug

admin.autodiscover()

urlpatterns = [
    path("", debug.default_urlconf),
    path("admin/", admin.site.urls),
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("weathapp/", include("weathapp.urls")),
    path("admin/", admin.site.urls),
]

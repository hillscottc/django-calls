from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("weathapp.urls")),  # Makes all root urls go to weathapp
    path("weathapp/", include("weathapp.urls")),
    path("admin/", admin.site.urls),
]

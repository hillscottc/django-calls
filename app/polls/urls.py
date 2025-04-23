from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("async/", views.my_async_view, name="my_async_view"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("weather/<int:zip>/", views.weather, name="weather"),
    path("send_all/", views.send_all, name="send_all"),
]

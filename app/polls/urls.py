from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.async_user_list, name="async_user_list"),
    path("users/", views.UsersView.as_view(), name="user_list"),
    path("weather_call/<str:zip>/<str:phone>",
         views.weather_call, name="weather_call"),
    path("send_all/", views.send_all, name="send_all"),
]

from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("async/", views.my_async_view, name="my_async_view"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    path("weather/<int:zip>/", views.weather, name="weather"),
    path("send_all/", views.send_all, name="send_all"),
    # path('wel/', views.ReactView.as_view(), name="something"),
]

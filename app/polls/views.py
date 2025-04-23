import requests
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from asgiref.sync import sync_to_async

from .models import Choice, Question, User
from .utils import get_weather, do_call
import logging

logger = logging.getLogger(__name__)


@sync_to_async
def get_users():
    return list(User.objects.all())


async def async_user_list(request):
    logger.info("Rendering user list page.")
    users = await get_users()
    context = {"users": users}
    return render(request, "polls/index.html", context)


class UsersView(generic.ListView):
    template_name = "polls/users.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return first 50 Users"""
        return User.objects.all()[:50]


def weather_call(request, zip):
    weather_results = get_weather(zip)
    twilio_results = do_call("+13104318777", weather_results)
    context = {"weather_results": weather_results,
               "twilio_results": twilio_results}
    return render(request, "polls/results.html", context)


async def send_all(request):
    users = await get_users()
    results = ""
    for user in users:
        weather_results = get_weather(user.zip)
        # twilio_results = do_call("+13104318777", weather_results)
        results += f"{weather_results}\n"

    context = {"results": results}
    return render(request, "polls/send-all-results.html", context)

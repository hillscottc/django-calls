from django.db.models import F
from django.shortcuts import render
from django.views import generic
from asgiref.sync import sync_to_async
from .models import AppUser
from .utils import get_weather, do_call

import logging
logger = logging.getLogger(__name__)


@sync_to_async
def get_users():
    return list(AppUser.objects.all())


async def async_user_list(request):
    logger.info("Rendering user list page.")
    users = await get_users()
    context = {"users": users}
    return render(request, "weathapp/index.html", context)


class UsersView(generic.ListView):
    template_name = "weathapp/users.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return first 50 Users"""
        return AppUser.objects.all()[:50]


def weather_call(request, zip, phone=''):
    weather_results = get_weather(zip)
    twilio_results = ""
    if phone:
        twilio_results = do_call(phone, weather_results)
    context = {"weather_results": weather_results,
               "twilio_results": twilio_results}
    return render(request, "weathapp/results.html", context)


async def send_all(request):
    users = await get_users()
    results_list = []
    for user in users:
        weather_results = get_weather(user.zip)
        twilio_results = do_call("+13104318777", weather_results)
        results_list.append(weather_results + " " + twilio_results)

    context = {"results_list": results_list}
    return render(request, "weathapp/send-all-results.html", context)

import requests
from django.db.models import F
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from asgiref.sync import sync_to_async

from .models import Choice, Question, User
from .utils import get_weather, do_call


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return first 50 Users"""
        return User.objects.all()[:50]


@sync_to_async
def get_users():
    return list(
        User.objects.all()
    )


async def my_async_view(request):
    users = await get_users()
    context = {"users": users}
    return render(request, "polls/my-async.html", context)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def weather(request, zip):
    weather_results = get_weather(zip)
    twilio_results = do_call("+13104318777", weather_results)
    context = {"weather_results": weather_results,
               "twilio_results": twilio_results}
    return render(request, "polls/results.html", context)


# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

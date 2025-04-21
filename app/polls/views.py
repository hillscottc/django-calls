import requests
from django.db.models import F
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def weather(request, zip):

    # 1. Geocoding API request
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={zip}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if geocoding_data and geocoding_data['results']:
        latitude = geocoding_data['results'][0]['latitude']
        longitude = geocoding_data['results'][0]['longitude']

        # 2. Weather API request
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        # return weather_data
        return JsonResponse(weather_data)
    else:
        return "Could not find location for that zip code."
    # response = "You're looking at the results of weather for zip %s."
    # return HttpResponse(response % zip)

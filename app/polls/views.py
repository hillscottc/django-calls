import requests
from django.db.models import F
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from .models import Choice, Question, User


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return first 50 Users"""
        return User.objects.all()[:50]


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

    # Geocoding API request to get the latitude, longitude, and city for given zip code
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={zip}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if geocoding_data and geocoding_data['results']:
        latitude = geocoding_data['results'][0]['latitude']
        longitude = geocoding_data['results'][0]['longitude']
        admin1 = geocoding_data['results'][0]['admin1']
        admin2 = geocoding_data['results'][0]['admin2']

        # Weather API request by lat/long
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
        weather_url = f"{weather_url}&temperature_unit=fahrenheit&current=temperature_2m,rain"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        # add the location to the data
        weather_data.update({'location': admin2 + ", " + admin1})

        # return JsonResponse(weather_data)
        response = f"In {weather_data['location']}, the current temperature is {weather_data['current']['temperature_2m']}°F, and rain is {weather_data['current']['rain']} inches."
        return HttpResponse(response)
    else:
        return "Could not find location for that zip code."

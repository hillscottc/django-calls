import requests
import os
from asgiref.sync import sync_to_async
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


def do_call(phone, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        twilio_message = client.messages.create(
            from_='+18333401082',
            body=message,
            to=phone
        )
        return twilio_message
    except Exception as e:
        err = f"Error sending message: {e}"
        print(err)
        return err


# @sync_to_async
def get_weather(zip):
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
        weather_results = f"In {weather_data['location']}, the current temperature is {weather_data['current']['temperature_2m']}°F, and rain is {weather_data['current']['rain']} inches."
    else:
        weather_results = "Could not find location for that zip code."
    return weather_results


@sync_to_async
def get_weather_async(zip):
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
        weather_results = f"In {weather_data['location']}, the current temperature is {weather_data['current']['temperature_2m']}°F, and rain is {weather_data['current']['rain']} inches."
    else:
        weather_results = "Could not find location for that zip code."
    return weather_results

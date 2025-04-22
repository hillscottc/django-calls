import requests
from twilio.rest import Client


def do_call(phone, message):
    account_sid = 'AC665861fdc9dca523f1f3b5300d7e5482'
    auth_token = '8413cf6d5408e07177d19e8e434c682d'
    client = Client(account_sid, auth_token)

    twilio_message = client.messages.create(
        from_='+18333401082',
        body=message,
        to=phone
    )
    return twilio_message


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

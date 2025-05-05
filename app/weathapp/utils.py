import requests
import os
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.environ.get("TWILIO_FROM_PHONE")


def brief_twilio(message):
    """
    Returns some key fields from Twilio message object, for convenience.
    """
    # return {
    #     "sid": message.sid,
    #     "from": message.from_,
    #     "to": message.to,
    #     "body": message.body,
    #     "status": message.status,
    #     "price": message.price if message.price else 'N/A',
    #     "error_message": message.error_message if message.error_message else 'N/A'
    # }
    return f"sid: {message.sid}, from: {message.from_}, to: {message.to}, status: {message.status}, price: {message.price if message.price else 'N/A'}, error_message: {message.error_message if message.error_message else 'N/A'}"


def do_call(phone, message):
    """
    Send a message to a phone number using Twilio.
    Args:
        phone (str): The phone number to send the message to.
        message (str): The message to send.
    Returns:
        str: The SID of the message sent.
    """
    logger.info(f"Sending text to {phone} from {TWILIO_FROM_PHONE}")
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        twilio_message = client.messages.create(
            from_=TWILIO_FROM_PHONE,
            body=message,
            to=phone
        )
        # return twilio_message
        return brief_twilio(twilio_message)
    except Exception as e:
        err = f"ERROR sending message. {e}"
        logger.error(err)
        return err


def get_weather(zip):
    """
    Get the weather for a given zip code using Open Meteo API.
    Args:
        zip (str): The zip code to get the weather for.
    Returns:
        str: The weather information for the given zip code.
    """

    # Geocoding API request to get the latitude, longitude, and city for given zip code
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={zip}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    try:
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
            weather_results = "Could not get weather for zip %s" % zip
    except Exception as e:
        err = f"Error sending message: {e}"
        weather_results = "Could not get weather for zip %s" % zip
        logger.error(err)
    logger.info(f"Weather for {zip} : {weather_results}")
    return weather_results

# WeatherApp - Django and MySQL on Docker

## The Task

Create a Django app that will allow multiple users to schedule wake-up calls that also announce the current weather based on their zip code. Communication should be done using Twilio [...see the rest...](https://docs.google.com/document/d/1qeaZR55AEINRRDYHk246DJCy_8DFyvHhvzIxED8naTc/edit?usp=sharing)

Weather is fetched from [Open-meteo](https://open-meteo.com/)

## API exposed by this app

Weather only: /polls/weather_call/{zip_code}

Weather, and text it: /polls/weather_call/{zip_code}/{phone_number}

Weather and text EVERYBODY: /polls/send_all

## Build and run locally

1. Run `docker compose --env-file .env.dev up --build`

2. Create superuser : `docker exec -it django-web python manage.py createsuperuser`

3. Visit `http://localhost:8000/polls` or `http://localhost:8000/admin`

4. Observe logging by running `docker logs -f django-web`

5. Data can be loaded via fixture: `python manage.py loaddata users.json`

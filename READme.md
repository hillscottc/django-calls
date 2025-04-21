# Django and MySQL on Docker

## Usage

1. Run `docker compose --env-file .env.dev up --build`

2. Create superuser : `docker exec -it django-web python manage.py createsuperuser`

3. Visit `http://localhost:8000` or `http://localhost:8000/admin`

Weather from https://open-meteo.com/en/docs

## The Task

Create a Django app that will allow multiple users to schedule wake-up calls that also announce the current weather based on their zip code. Communication should be done using Twilio.

- The wake-up call can be either a call or a text message based on the user's preference. Either version should be able to accept changing the next scheduled time, stopping, or switching the contact method.
  -Call version can use voice input or DTMF.

Scheduling a new wake-up call can be done in multiple ways.

- Using the app
- External API for extensibility.
- (Optional) Inbound Call to the system.
- Before the wake-up calls can be executed, the user's phone number should be verified for ownership.

The project should:

- Run in a container with instructions to build and deploy to the AWS Fargate service.
- Log to AWS CloudWatch
- Use a Git Repo
- Async requests use a queueing service.
- Include a tool to seed the data for at least 30 demo events. Demo events can be suppressed from making actual calls/text messages, but should be logged.
- Demonstrate user and admin roles.

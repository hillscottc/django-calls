# Django and MySQL on Docker

1. Run `docker compose --env-file .env.dev up --build`

2. Create superuser : `docker exec -it django-web python manage.py createsuperuser`

3. Visit `http://localhost:8000` or `http://localhost:8000/admin`

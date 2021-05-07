web: gunicorn zuri_django.wsgi --log-file -
release: python manage.py migrate
release: python manage.py collectstatic
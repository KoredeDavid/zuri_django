web: gunicorn zuri_django.wsgi --log-file -
release: python manage.py collectstatic --no-input
release: python manage.py migrate
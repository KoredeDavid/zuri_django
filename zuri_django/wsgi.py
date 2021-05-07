"""
WSGI config for zuri_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('DJANGO_ENV', '') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zuri_django.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zuri_django.settings.dev')
application = get_wsgi_application()



from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'TRUE')

ALLOWED_HOSTS = ['blogzuri.herokuapp.com', '127.0.0.1']

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME', ''),
        'USER': os.environ.get('DBUSER', ''),
        'PASSWORD': os.environ.get('DBPASS', ''),
        'HOST': os.environ.get('DBHOST', ''),
        'PORT': os.environ.get('DBPORT', ''),

    }
}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SERVER_EMAIL = os.environ.get('SERVER_EMAIL', "")
DEFAULT_FROM_EMAIL = SERVER_EMAIL

ADMINS = [
    ('KoredeDavid', os.environ.get('EMAIL', "")),
    ('Conceal', SERVER_EMAIL),
]

MANAGERS = ADMINS

import dj_database_url

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

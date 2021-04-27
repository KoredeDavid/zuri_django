from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '@6n7rh6c=vpc*kf%8+x+vg8w&pu$#bh+*@16p3q@cd*)*rf*5#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('sslserver', )

BASE_DIR = os.getcwd()

# DATABASE settings uses sqlite when sqlite is set to true but uses Postgres if not
sqlite = True

if sqlite:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'conceal',
            'USER': 'postgres',
            'PASSWORD': 'Davdam@50.',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVER_EMAIL = 'test@gmail.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

ADMINS = [
    ('KoredeDavid', 'test@gmail.com'),
    ('Conceal', 'test@gmail.com'),
]

MANAGERS = ADMINS
 
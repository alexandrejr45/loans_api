from loans_api.settings.base import *

BASE_DIR = BASE_DIR

SECRET_KEY = 'X+fr>_My+-JXpbNg;4[us2R4YV23U3u/2L[u2xqw[[yjAww[E(qJ*7hpSxHj:=:dg=P'

DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

from .base import *

import dj_database_url


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Heroku
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
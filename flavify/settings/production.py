from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Heroku
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
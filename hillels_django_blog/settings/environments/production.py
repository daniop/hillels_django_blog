from hillels_django_blog.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
)

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'hillels_django_blog.herokuapp.com']

MIDDLEWARE += (
    'whitenoise.middleware.WhiteNoiseMiddleware'
)

INSTALLED_APPS += (
    'whitenoise.runserver_nostatic'
)


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

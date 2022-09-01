from hillels_django_blog.settings.components.common import (
    MIDDLEWARE,
)

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'hillels_django_blog.herokuapp.com']

MIDDLEWARE += (
    'whitenoise.middleware.WhiteNoiseMiddleware'
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import os

from hillels_django_blog.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dani',
        'USER': 'dani',
        'PASSWORD': '',
        'HOST': 'localhost'
    }
}

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS = []

# Installed apps for development only:

INSTALLED_APPS += (
    'django_extensions',
    "debug_toolbar",
)

# Static and media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    'blog/static',
]

MEDIA_ROOT = os.path.join('media')
MEDIA_URL = 'media/'

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

# Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CASHES and CELERY

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
from os import environ

from split_settings.tools import include

ENV = environ.get('DJANGO_ENV') or 'development'

base_settings = [
    'components/common.py',  # standard django settings
    'components/celery.py',
    'components/database.py',  # redis and redis-queue
    # 'components/emails.py',  # smtp

    # Select the right env:
    'environments/{0}.py'.format(ENV),
]

# Include settings:
include(*base_settings)

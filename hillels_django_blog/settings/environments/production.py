import os

import dj_database_url


DATABASES = {}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'] = db_from_env

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'hillels-django-blog.herokuapp.com']

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = os.environ.get('REDIS_URL')

# AWS S3 SETTINGS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.environ.get('AWS_URL')
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = False

MEDIA_URL = AWS_URL + '/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# URL
SCHEMA = 'https'

DOMAIN = "hillels-django-blog.herokuapp.com"

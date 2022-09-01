import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hillels_django_blog.settings')

app = Celery('hillels_django_blog')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  # noqa: T201

from celery import Celery
from celery.signals import setup_logging
from celery.schedules import crontab
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sibdev_test.settings')

app = Celery('sibdev_test')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'collect_daily_quotes': {
        'task': 'collect_daily_quotes',
        'schedule': crontab(minute='0', hour='12'),
    },
    'check_threshold': {
        'task': 'check_threshold',
        'schedule': crontab(minute='5', hour='12'),
    },
}


@setup_logging.connect()
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    dictConfig(settings.LOGGING)

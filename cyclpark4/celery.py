from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import django
from cyclpark4 import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyclpark4.settings')
django.setup()
app = Celery('cyclpark4')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.update(result_expires=3600, enable_utc=True, timezone='UTC')
app.conf.beat_shedule = {
    'update-points-task': {
        'task': 'main.tasks.update_points_task',
        'schedule': crontab()
    }
}

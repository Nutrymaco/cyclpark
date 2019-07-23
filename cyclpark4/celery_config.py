from celery import Celery
from celery.schedules import crontab


class Config:
    timezone = 'Europe/Moscow'
    enable_utc = True

    task_always_eager = False
    broker_url = 'amqp://localhost:5672'
    result_expires = 3600
    worker_prefetch_multiplier = 1
    worker_max_memory_per_child = 250000  # 250MB

    beat_schedule = {
        'update-points-task': {
            'task': 'main.tasks.update_points_task',
            'schedule': crontab(hour='*/12')
        }
    }
    worker_hijack_root_logger = False
    accept_content = ['json']


app = Celery()
app.config_from_object(Config)

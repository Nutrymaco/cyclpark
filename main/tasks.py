from .update import update_points
from cyclpark4.celery_config import app
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)
django.setup()


@app.task
def update_points_task():
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)
    import django
    django.setup()
    print('Апдейтнулось')
    update_points()

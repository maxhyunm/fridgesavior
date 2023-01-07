from __future__ import absolute_import, unicode_literals
import os
from rest_framework.response import Response
from celery import Celery
from celery.schedules import crontab
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fridgeback.settings')
os.environ.setdefault('CELERY_ALWAYS_EAGER', 'False')

app = Celery('fridgeback')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    timezone='Asia/Seoul',
    broker_pool_limit=None,
    result_expires=86400,
)

app.conf.beat_schedule = {
    'check-expire-dates': {
        'task': 'items.tasks.check_expire_dates',
        'schedule': crontab(hour=9, minute=0),
        'args': (),
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Require: {0!r}'.format(self.request))
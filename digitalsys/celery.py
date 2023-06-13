import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digitalsys.settings")

app = Celery("digitalsys")

CELERY_BEAT_SCHEDULE = {
    "change_status": {
        "task": "digitalsys.api.tasks.change_status",
        "schedule": crontab(minute="*/1"),
    },
}
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

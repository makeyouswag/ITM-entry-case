import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


class DBRetryCelery(Celery):
    def __init__(self, *args, **kwargs):
        from time import sleep

        from django.conf import settings
        from django.db import connection
        from django.db.utils import OperationalError

        while True:
            try:
                cursor = connection.cursor()
                cursor.close()
                break
            except OperationalError as e:
                print(f"{e} (retry after {settings.RECONNECT_INTERVAL} seconds)")
                sleep(settings.RECONNECT_INTERVAL)

        super().__init__(*args, **kwargs)


app = DBRetryCelery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.task_always_eager = True

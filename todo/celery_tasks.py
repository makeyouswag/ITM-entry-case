from core.celery import app
from task import models


def send_mail(message):
    pass


@app.task()
def send_mail_task_changed_status(instance_id: int):
    instance = models.Task.objects.get(id=instance_id)
    message = f"Task {instance.title} has changed state to {instance.state}"
    send_mail(message)
    print("Message is sent")
from django.db.models import Prefetch
from rest_framework import generics, viewsets, mixins
from task import models, serializers
from task.celery_tasks import send_mail_task_changed_status


class TaskListCreate(generics.ListCreateAPIView):
    queryset = models.Task.objects.prefetch_related('groups')

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.TaskWriteSerializer
        return serializers.TaskReadSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Task.objects.all()

    def perform_update(self, serializer: serializers.TaskWriteSerializer):
        initial_state = serializer.instance.state
        instance = serializer.save()
        if initial_state != instance.state:
            send_mail_task_changed_status.apply_async(kwargs={"instance_id": instance.id})

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.TaskReadSerializer
        return serializers.TaskWriteSerializer


class GroupViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer



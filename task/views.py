from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from task import models, serializers
from task.celery_tasks import send_mail_task_changed_status
from task.serializers import TaskReadSerializer


def validate_incoming_state(state: str) -> bool:
    return state in ("todo", "in_progress", "completed")


class TaskListCreate(generics.ListCreateAPIView):
    queryset = models.Task.objects.all()

    def post(self, request, *args, **kwargs):
        """Оверрайд для валидации статуса."""
        state_is_valid = validate_incoming_state(request.data["state"])
        if not state_is_valid:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return  super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.TaskWriteSerializer
        return TaskReadSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Task.objects.all()

    def patch(self, request, *args, **kwargs):
        state_is_valid = validate_incoming_state(request.data["state"])
        if not state_is_valid:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().patch(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        """Оверрайд для валидации статуса."""
        state_is_valid = validate_incoming_state(request.data["state"])
        if not state_is_valid:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Оверрайд для валидации статуса."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        initial_state = instance.state
        self.perform_update(serializer)
        if initial_state != instance.state:
            send_mail_task_changed_status.apply_async(kwargs={"instance":instance})
        return Response(serializer.data)

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



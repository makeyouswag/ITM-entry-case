from rest_framework import serializers
from task import models


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = '__all__'


class TaskBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ("id", 'title', "description", 'state',)


class TaskReadSerializer(TaskBaseSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.Task
        fields = ("id", 'title', "description", 'state', 'groups')


class TaskWriteSerializer(TaskBaseSerializer):
    pass
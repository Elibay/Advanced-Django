from core.models import Project, Task
from rest_framework import serializers

from users.serializers import UserSerializer


class ProjectShortSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    status_name = serializers.SerializerMethodField

    class Meta:
        model = Project
        fields = ('id', 'name', 'status', 'creator')

    def validate_status(self, value):
        if value > 3 or value < 1:
            raise serializers.ValidationError('Project status must be between 1 and 3')
        return value

    def validate_id(self, value):
        if value > 0:
            raise serializers.ValidationError('Project status must be geater than 0')
        return value


class ProjectSerializer(ProjectShortSerializer):
    class Meta:
        fields = '__all__'


class TaskShortSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'creator', 'name', 'status')


class TaskSerializer(TaskShortSerializer):
    executor = UserSerializer(read_only=True)

    class Meta:
        fields = '__all__'

    def validate_order(self, value):
        if value < 0:
            raise serializers.ValidationError('Positive number')
        return value


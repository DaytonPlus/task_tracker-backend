from rest_framework import serializers
from.models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'objectives', 'start_date', 'end_date']
        read_only_fields = ['id']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'assigned_to', 'start_date', 'end_date', 'status']
        read_only_fields = ['id']

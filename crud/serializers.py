from rest_framework import serializers
from.models import Project, Task

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'objectives', 'start_date', 'end_date', 'created_at', 'updated_at', 'created_by', 'updated_by']
        read_only_fields = ['id', 'created_at', 'created_by', 'updated_at']

    def create(self, validated_data):
        project = Project.objects.create(**validated_data, created_by=self.context['request'].user)
        return project

    def update(self, instance, validated_data):
        instance.updated_by = self.context['request'].user
        super().update(instance, validated_data)
        return instance


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'assigned_to', 'start_date', 'end_date', 'status', 'created_at', 'updated_at', 'created_by', 'updated_by']
        read_only_fields = ['id', 'created_at', 'created_by']

    def create(self, validated_data):
        task = Task.objects.create(**validated_data, created_by=self.context['request'].user, project=self.context['project'])
        return task

    def update(self, instance, validated_data):
        instance.updated_by = self.context['request'].user
        super().update(instance, validated_data)
        return instance

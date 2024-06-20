from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from.models import Project, Task
from.serializers import ProjectSerializer, TaskSerializer
from user.serializers import UserSerializer

class ProjectsView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            request.user.project = serializer.instance
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectJoinView(APIView):
    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        request.user.project = project
        request.user.save()
        return Response({"detail": "Joined the project"}, status=status.HTTP_200_OK)

class ProjectView(APIView):
    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
        
    def put(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return Response({"detail": "Project deleted successfully"}, status=status.HTTP_200_OK)

class TasksView(APIView):
    def get(self, request, project_id):
        tasks = Task.objects.filter(project=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = TaskSerializer(data=request.data, context={'request': request, 'project': project})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    def get(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, project_id=project_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, project_id=project_id)
        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, project_id=project_id)
        task.delete()
        return Response({"detail": "Task deleted successfully"}, status=status.HTTP_200_OK)

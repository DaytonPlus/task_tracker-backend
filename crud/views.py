from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.models import Project, Task
from.serializers import ProjectSerializer, TaskSerializer


class ProjectsView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectView(APIView):
    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response({"detail":"No Project matches the given query."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"detail":"No Project matches the given query."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
            project.delete()
            return Response({"detail": "Project deleted successfully"}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"detail":"No Project matches the given query."}, status=status.HTTP_404_NOT_FOUND)

class TasksView(APIView):
    def get(self, request, project_id):
        tasks = Task.objects.filter(project=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        request.data['project'] = project_id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    def get(self, request, project_id, task_id):
        task = Task.objects.get(pk=task_id, project_id=project_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, project_id, task_id):
        task = Task.objects.get(pk=task_id, project_id=project_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, task_id):
        try:
            task = Task.objects.get(pk=task_id, project_id=project_id)
            task.delete()
            return Response({"detail": "Task deleted successfully"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"detail": "No Task matches the given query."}, status=status.HTTP_404_NOT_FOUND)

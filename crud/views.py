from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from.models import Project, Task
from.serializers import ProjectSerializer, TaskSerializer
from user.serializers import UserSerializer

class ProjectsView(APIView):
    def get(self, request, project_id):
        projects = Project.objects.all()
        query = request.query_params
        fields = Project._meta.get_fields()
        if len(query) > 0:
            q = Q()
            for key, value in query.items():
                if key in [field.name for field in fields if not field.is_relation]:
                    q &= Q(**{key: value})
            projects = projects.filter(q)
        orderby = query.get('orderby', None)
        if orderby and orderby in [field.name for field in fields if not field.is_relation]:
            projects = projects.order_by(orderby)
        serializer = TaskSerializer(projects, many=True)
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
        if project == request.user.project:
            return Response({"detail": "Ya estas en este proyecto"}, status=status.HTTP_400_BAD_REQUEST)
        request.user.project = project
        request.user.save()
        return Response({"detail": f"Te has unido al proyecto {project_id}"}, status=status.HTTP_200_OK)

class ProjectLeaveView(APIView):
    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if project == request.user.project:
            request.user.project = None
            request.user.save()
            return Response({"detail": "Has dejado de ser miembro de este proyecto"})
        return Response({"detail": "Tu no eres miembro de este proyecto"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"detail": f"El proyecto {project_id} ha sido eliminado"})

class TasksView(APIView):
    def get(self, request, project_id):
        tasks = Task.objects.filter(project=project_id)
        query = request.query_params
        fields = Project._meta.get_fields()
        if len(query) > 0:
            q = Q()
            for key, value in query.items():
                if key in [field.name for field in fields if not field.is_relation]:
                    q &= Q(**{key: value})
            tasks = tasks.filter(q)
        orderby = query.get('orderby', None)
        if orderby and orderby in [field.name for field in fields if not field.is_relation]:
            projects = projects.order_by(orderby)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        if request.data and request.data['status']:
            del request.data['status']
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
        return Response({"detail": f"La tarea {task_id} ha sido eliminada"})

class TaskAssignView(APIView):
    def post(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, project_id=project_id)
        if task.status in ["closed", "resolved"]:
            return Response({"detail": f"No puedes unirte a la tarea {task_id}"}, status=status.HTTP_400_BAD_REQUEST)
        task.assigned_to = request.user
        task.status = "assigned"
        task.save()
        return Response({"detail": f"Has sido asignado a la tarea {task_id}"})

class TaskUnassignView(APIView):
    def post(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, project_id=project_id)
        if task.status in ["closed", "resolved"]:
            return Response({"detail": f"No puedes salir de la tarea {task_id}"}, status=status.HTTP_400_BAD_REQUEST)
        task.assigned_to = None
        task.status = "new"
        task.save()
        return Response({"detail": f"Has sido desasignado a la tarea {task_id}"})

class TaskCloseView(APIView):
    def post(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, project_id=project_id)
        if task.status == "resolved":
            return Response({"detail": f"La tarea {task_id} ya ha sido terminada"}, status=status.HTTP_400_BAD_REQUEST)
        task.status = "closed"
        task.save()
        return Response({"detail": "La tarea {task_id} ha sido cerrada"})

class TaskResolveView(APIView):
    def post(self, request, project_id, task_id):
        task = get_object_or_404(Task, pk=task_id, project_id=project_id)
        if task.status == "closed":
            return Response({"detail": f"La tarea {task_id} ya ha sido cerrada"}, status=status.HTTP_400_BAD_REQUEST)
        task.status = "resolved"
        task.save()
        return Response({"detail": f"La tarea {task_id} ha sido terminada"})



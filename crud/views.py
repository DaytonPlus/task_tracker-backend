from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Project, TeamMember, Task
from .serializers import ProjectSerializer, TeamMemberSerializer, TaskSerializer

class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

class TeamMemberView(ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

class TaskView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]



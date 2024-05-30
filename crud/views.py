from django.shortcuts import render
from rest_framework import viewsets, permissions 
from .models import Project, TeamMember, Task
from .serializers import ProjectSerializer, TeamMemberSerializer, TaskSerializer

# Create your views here.


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer

class TeamMemberView(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TeamMemberSerializer

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TaskSerializer



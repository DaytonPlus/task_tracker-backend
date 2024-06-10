from django.urls import path
from.views import ProjectsView, ProjectView, TasksView, TaskView

urlpatterns = [
    path('projects/', ProjectsView.as_view()),
    path('projects/<int:project_id>/', ProjectView.as_view()),
    path('projects/<int:project_id>/tasks/', TasksView.as_view()),
    path('projects/<int:project_id>/tasks/<int:task_id>/', TaskView.as_view()),
]

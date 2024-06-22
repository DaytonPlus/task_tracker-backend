from django.urls import path
from .views import ProjectsView, ProjectView, ProjectJoinView, TasksView, TaskView, TaskAssignView, TaskUnassignView, TaskCloseView, TaskResolveView
from.exports import ExportXLSView, ExportPDFView

urlpatterns = [
    path('exports/xls/', ExportXLSView.as_view()),
    path('exports/pdf/', ExportPDFView.as_view()),
    path('projects/', ProjectsView.as_view()),
    path('projects/<int:project_id>/', ProjectView.as_view()),
    path('projects/<int:project_id>/join/', ProjectJoinView.as_view()),
    path('projects/<int:project_id>/tasks/', TasksView.as_view()),
    path('projects/<int:project_id>/tasks/<int:task_id>/', TaskView.as_view()),
    path('projects/<int:project_id>/tasks/<int:task_id>/assign/', TaskAssignView.as_view()),
    path('projects/<int:project_id>/tasks/<int:task_id>/unassign/', TaskUnassignView.as_view()),
    path('projects/<int:project_id>/tasks/<int:task_id>/resolve/', TaskResolveView.as_view()),
    path('projects/<int:project_id>/tasks/<int:task_id>/close/', TaskCloseView.as_view()),
]

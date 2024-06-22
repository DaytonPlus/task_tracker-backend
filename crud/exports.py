# -*- coding: utf-8 -*- 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from openpyxl import Workbook
from weasyprint import HTML, CSS
from io import BytesIO
from user.models import User
from.models import Project, Task

from datetime import datetime

css = [CSS(string='''
body {
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;
  color: #333;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 500;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

dl {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

dt {
  font-weight: bold;
  text-align: left;
  padding-right: 1rem;
}

dd {
  margin-left: 0;
}

@media print {
  body {
    background-color: white;
    color: black;
  }

  dl {
    font-size: 0.8rem;
  }

  h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid;
  }
}
''')]

def generateHTMl():
    projects = Project.objects.all()
    tasks = Task.objects.all()
    html = "<html><body>"

    html += "<h1>Proyectos</h1>"

    for project in projects:
        try:
            created_by = User.objects.get(id=project.created_by).username
        except User.DoesNotExist:
            created_by = "-"
        try:
            updated_by = User.objects.get(id=project.updated_by).username
        except User.DoesNotExist:
            updated_by = "-"

        created_at = project.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
        updated_at = project.updated_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')

        html += "<dl>"
        html += f"<dt>ID</dt><dd>{project.id}</dd>"
        html += f"<dt>Nombre</dt><dd>{project.name}</dd>"
        html += f"<dt>Descripción</dt><dd>{project.description}</dd>"
        html += f"<dt>Objetivos</dt><dd>{project.objectives}</dd>"
        html += f"<dt>Fecha Inicio</dt><dd>{project.start_date}</dd>"
        html += f"<dt>Fecha Fin</dt><dd>{project.end_date}</dd>"
        html += f"<dt>Creado En</dt><dd>{created_at}</dd>"
        html += f"<dt>Actualizado En</dt><dd>{updated_at}</dd>"
        html += f"<dt>Creado Por</dt><dd>{created_by}</dd>"
        html += f"<dt>Actualizado Por</dt><dd>{updated_by}</dd>"
        html += "</dl>"

    html += "<h1>Tareas</h1>"

    for task in tasks:
        try:
            assigned_to = User.objects.get(id=task.assigned_to).username
        except User.DoesNotExist:
            assigned_to = "-"
        try:
            created_by = User.objects.get(id=task.created_by).username
        except User.DoesNotExist:
            created_by = "-"
        try:
            updated_by = User.objects.get(id=task.updated_by).username
        except User.DoesNotExist:
            updated_by = "-"
        try:
            project = Project.objects.get(id=task.project).name
        except Project.DoesNotExist:
            project = "-"
    
        created_at = task.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
        updated_at = task.updated_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
    
        html += "<dl>"
        html += f"<dt>ID</dt><dd>{task.id}</dd>"
        html += f"<dt>From Project</dt><dd>{project}</dd>"
        html += f"<dt>Nombre</dt><dd>{task.name}</dd>"
        html += f"<dt>Descripción</dt><dd>{task.description}</dd>"
        html += f"<dt>Asignado A</dt><dd>{assigned_to}</dd>"
        html += f"<dt>Fecha Inicio</dt><dd>{task.start_date}</dd>"
        html += f"<dt>Fecha Fin</dt><dd>{task.end_date}</dd>"
        html += f"<dt>Estado</dt><dd>{task.status}</dd>"
        html += f"<dt>Creado En</dt><dd>{created_at}</dd>"
        html += f"<dt>Actualizado En</dt><dd>{updated_at}</dd>"
        html += f"<dt>Creado Por</dt><dd>{created_by}</dd>"
        html += f"<dt>Actualizado Por</dt><dd>{updated_by}</dd>"
        html += "</dl>"
    html += "</body></html>"
    return HTML(string=html)


class ExportXLSView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        workbook = Workbook()

        worksheet = workbook.active
        worksheet.title = "Projects"
        projects = Project.objects.all()
        worksheet.append(['id', 'name', 'description', 'objectives', 'start_date', 'end_date', 'created_at', 'updated_at', 'created_by', 'updated_by'])
        for project in projects:
            try:
                created_by = User.objects.get(id=project.created_by).username
            except User.DoesNotExist:
                created_by = "- unknown -"
            try:
                updated_by = User.objects.get(id=project.updated_by).username
            except User.DoesNotExist:
                updated_by = "- not updated  -"

            created_at = project.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
            updated_at = project.updated_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')

            worksheet.append([project.id, project.name, project.description, project.objectives, project.start_date, project.end_date, created_at, updated_at, created_by, updated_by])
        
        worksheet_tasks = workbook.create_sheet("Tasks")
        tasks = Task.objects.all()
        worksheet_tasks.append(['id', 'from-project', 'name', 'description', 'assigned_to', 'start_date', 'end_date', 'status', 'created_at', 'updated_at', 'created_by', 'updated_by'])
        for task in tasks:
            try:
                assigned_to = User.objects.get(id=task.assigned_to).username
            except User.DoesNotExist:
                assigned_to = "-"
            try:
                created_by = User.objects.get(id=task.created_by).username
            except User.DoesNotExist:
                created_by = "-"
            try:
                updated_by = User.objects.get(id=task.updated_by).username
            except User.DoesNotExist:
                updated_by = "-"
            try:
                project = Project.objects.get(id=task.project).name
            except Project.DoesNotExist:
                project = "-"

            created_at = task.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
            updated_at = task.updated_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')

            worksheet_tasks.append([task.id, project, task.name, task.description, assigned_to, task.start_date, task.end_date, task.status, created_at, updated_at, created_by, updated_by])

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename='projects_and_tasks.xlsx'"
        workbook.save(response)
        return response

class ExportPDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        file = BytesIO()
        html = generateHTMl()
        html.write_pdf(file, stylesheets=css)
        response = HttpResponse(file.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename='projects_and_tasks.pdf'"
        return response

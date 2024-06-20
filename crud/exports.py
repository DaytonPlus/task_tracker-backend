from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from openpyxl import Workbook
from weasyprint import HTML
from io import BytesIO
from user.models import User
from.models import Project, Task

from datetime import datetime


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
        worksheet_tasks.append(['id', 'name', 'description', 'assigned_to', 'start_date', 'end_date', 'status', 'created_at', 'updated_at', 'created_by', 'updated_by'])
        for task in tasks:
            try:
                assigned_to = User.objects.get(id=task.assigned_to).username
            except User.DoesNotExist:
                assigned_to = "- desconocido -"
            try:
                created_by = User.objects.get(id=task.created_by).username
            except User.DoesNotExist:
                created_by = "- desconocido -"
            try:
                updated_by = User.objects.get(id=task.updated_by).username
            except User.DoesNotExist:
                updated_by = "-----"

            created_at = task.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
            updated_at = task.updated_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')

            worksheet_tasks.append([task.id, task.name, task.description, assigned_to, task.start_date, task.end_date, task.status, created_at, updated_at, created_by, updated_by])

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename='projects_and_tasks.xlsx'"
        workbook.save(response)
        return response

class ExportPDFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        projects = Project.objects.all()
        tasks = Task.objects.all()
        html = "<html><body>"
        html += "<h1>Proyectos</h1>"
        html += "<table border='1'>"
        html += "<tr><th>ID</th><th>Nombre</th><th>Descripcion</th><th>Objetivos</th><th>Fecha Inicio</th><th>Fecha Fin</th><th>Creado En</th><th>Actualizado En</th><th>Creado Por</th><th>Actualizado Por</th></tr>"
        for project in projects:
            try:
                created_by = User.objects.get(id=project.created_by).username
            except User.DoesNotExist:
                created_by = "- desconocido -"
            try:
                updated_by = User.objects.get(id=project.updated_by).username
            except User.DoesNotExist:
                updated_by = "- desconocido -"

            created_at = project.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
            updated_at = project.updated_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')

            html += "<tr>"
            html += f"<td>{project.id}</td>"
            html += f"<td>{project.name}</td>"
            html += f"<td>{project.description}</td>"
            html += f"<td>{project.objectives}</td>"
            html += f"<td>{project.start_date}</td>"
            html += f"<td>{project.end_date}</td>"
            html += f"<td>{created_at}</td>"
            html += f"<td>{updated_at}</td>"
            html += f"<td>{created_by}</td>"
            html += f"<td>{updated_by}</td>"
            html += "</tr>"
        html += "</table>"

        html += "<h1>Tareas</h1>"
        html += "<table border='1'>"
        html += "<tr><th>ID</th><th>Nombre</th><th>Descripcion</th><th>Asignado A</th><th>Fecha Inicio</th><th>Fecha Fin</th><th>Estado</th><th>Creado En</th><th>Actualizado En</th><th>Creado Por</th><th>Actualizado Por</th></tr>"
        for task in tasks:
            try:
                assigned_to = User.objects.get(id=task.assigned_to).username
            except User.DoesNotExist:
                assigned_to = "- desconocido -"
            try:
                created_by = User.objects.get(id=task.created_by).username
            except User.DoesNotExist:
                created_by = "- desconocido -"
            try:
                updated_by = User.objects.get(id=task.updated_by).username
            except User.DoesNotExist:
                updated_by = "- desconocido -"

            created_at = task.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
            updated_at = task.updated_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')

            html += "<tr>"
            html += f"<td>{task.id}</td>"
            html += f"<td>{task.name}</td>"
            html += f"<td>{task.description}</td>"
            html += f"<td>{assigned_to}</td>"
            html += f"<td>{task.start_date}</td>"
            html += f"<td>{task.end_date}</td>"
            html += f"<td>{task.status}</td>"
            html += f"<td>{created_at}</td>"
            html += f"<td>{updated_at}</td>"
            html += f"<td>{created_by}</td>"
            html += f"<td>{updated_by}</td>"
            html += "</tr>"

        html += "</table>"
        html += "</body></html>"
        file = BytesIO()
        html = HTML(string=html)
        html.write_pdf(file)
        response = HttpResponse(file.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename='projects_and_tasks.pdf'"
        return response
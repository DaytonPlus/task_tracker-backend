from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    objectives = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TeamMember(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    identification_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey('TeamMember', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Nueva', 'Nueva'),
        ('Asignada', 'Asignada'),
        ('Aceptada', 'Aceptada'),
        ('Resuelta', 'Resuelta'),
        ('Cerrada', 'Cerrada')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

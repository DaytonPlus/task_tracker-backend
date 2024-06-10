from django.db import models
from django.core.validators import MinLengthValidator
# from django.utils import timezone
from.choices import STATUS_CHOICES


class Project(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(3)], unique=True)
    description = models.TextField()
    objectives = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, validators=[MinLengthValidator(1)], unique=True)
    description = models.TextField()
    assigned_to = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    
    def __str__(self):
        return self.name

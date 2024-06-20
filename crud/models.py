from django.db import models
from django.core.validators import MinLengthValidator
from.choices import STATUS_CHOICES


class Project(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(3)], unique=True)
    description = models.TextField(max_length=255)
    objectives = models.TextField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            kwargs.get('request').user.project = self
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, validators=[MinLengthValidator(1)], unique=True)
    description = models.TextField(max_length=255)
    assigned_to = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
 
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            kwargs.get('request').user.project = self
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

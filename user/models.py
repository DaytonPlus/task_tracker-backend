from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from rest_framework.authtoken.models import Token as RFToken
from.choices import ROLE_CHOICES, GENDER_CHOICES
from django.core.validators import MinLengthValidator

class CustomUserManager(UserManager):
    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return super().create_superuser(**extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50, validators=[MinLengthValidator(3)], unique=True)
    full_name = models.CharField(max_length=150)
    identification_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    project = models.ForeignKey('crud.Project', on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions_set')
    objects = CustomUserManager()
    is_admin = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'identification_number', 'email', 'contact_number', 'gender', 'role']
    
    def __str__(self):
        return self.username

class Token(RFToken):
    # user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='token')
    
    def __str__(self):
        return "Token for user ${self.user.username}"

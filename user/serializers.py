from rest_framework import serializers
from.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'identification_number', 'email', 'contact_number', 'gender', 'project', 'role', 'is_admin']
        read_only_fields = ['id', 'is_admin', 'is_superuser']

class RegUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'is_admin', 'is_superuser', 'groups', 'user_permissions']

class SuUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'is_superuser', 'groups', 'user_permissions']


from rest_framework import serializers
from.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'identification_number', 'email', 'contact_number', 'gender', 'project', 'role']
        read_only_fields = ['id']

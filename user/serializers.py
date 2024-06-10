from rest_framework import serializers
from.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'identification_number', 'email', 'contact_number', 'gender', 'project', 'role', 'is_admin', 'is_superuser']
        read_only_fields = ['id', 'is_admin', 'is_superuser']
        
        def update(self, instance, validated_data):
            for field, value in validated_data.items():
                if getattr(instance, field)!= value:
                    setattr(instance, field, value)
            instance.save()
            return instance

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
        
        def update(self, instance, validated_data):
            for field, value in validated_data.items():
                if getattr(instance, field)!= value:
                    setattr(instance, field, value)
            instance.save()
            return instance


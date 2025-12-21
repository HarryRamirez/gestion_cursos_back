from apps.users.models import User, Role
from django.contrib.auth.models import Group
from rest_framework import serializers




class GetUserSerializer(serializers.ModelSerializer):
    
    role = serializers.StringRelatedField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active','date_joined', 'role']




class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.exclude(name='admin')
    )

    def create(self, validated_data):
        role = validated_data['role']
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role,
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Asignamos Group según el Role
        try:
            group = Group.objects.get(name=role.name.capitalize())
            user.groups.add(group)
        except Group.DoesNotExist:
            pass  
        
        return user


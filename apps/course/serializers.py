from rest_framework import serializers
from .models import Course




class GetListCourseSerializer(serializers.ModelSerializer):
    
    category = serializers.StringRelatedField()
    instructor = serializers.StringRelatedField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'status', 'is_active', 'created_at', 'category', 'instructor']



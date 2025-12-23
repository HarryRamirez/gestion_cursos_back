from rest_framework import serializers
from apps.course.models import Enrollment



class EnrollmentListSerializer(serializers.ModelSerializer):
    
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'status']
        





class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']
        validators = []
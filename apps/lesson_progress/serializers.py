from rest_framework import serializers
from apps.course.models import LessonProgress




class LessonProgressListSerializer(serializers.ModelSerializer):
    
    student = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()
    
    class Meta:
        model = LessonProgress
        fields = ['id', 'student', 'lesson', 'progress', 'completed', 'updated_at']



class LessonProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson', 'progress', 'completed', 'updated_at']
        read_only_fields = ['lesson', 'updated_at']

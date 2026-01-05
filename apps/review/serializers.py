from rest_framework import serializers
from apps.course.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    
    
    class Meta:
        model = Review
        fields = ['id', 'student', 'course', 'rating', 'comment', 'created_at']
        


class ReviewCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['course', 'rating', 'comment']
        





class ReviewUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment']
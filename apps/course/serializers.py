from rest_framework import serializers
from .models import Course, Lesson
from django.db import transaction




class LessonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'order']
        read_only_fields = ['order']


class CourseListSerializer(serializers.ModelSerializer):
    
    category = serializers.StringRelatedField()
    instructor = serializers.StringRelatedField()
    lessons = LessonSerializer(many=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'status', 'is_active', 'created_at', 'category', 'instructor','lessons']




# Se crea el curso y se la agraga el order incremental segun de las lessiones
# tambien se agrega la transaccion para que solo se ejecute si todo esta bien 
# esto para que no queden relaciones huerfanas
class CourseLessonCreateSerializer(serializers.ModelSerializer):
    
    lessons = LessonSerializer(many=True,  required=False)
    
    class Meta:
        model = Course
        fields = ['title', 'description', 'status', 'category', 'lessons']
    
    
    def create(self, validated_data):
        
        request = self.context['request']
        instructor = request.user
        lessons_data = validated_data.pop('lessons', [])

        with transaction.atomic():
            course = Course.objects.create(instructor=instructor, **validated_data)

            for index, lesson_data in enumerate(lessons_data, start=1):
                Lesson.objects.create(
                    course=course,
                    order=index,
                    **lesson_data
                )

        return course



class CourseUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['title', 'description', 'status', 'category']
from rest_framework import serializers
from apps.course.models import Lesson
from django.db.models import Max



class LessonListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'created_at', 'order']





class LessonCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content']
        
        
    def create(self, validated_data):
        course = validated_data['course']

        # obtenemos el numero mayor del order y la gargamos 1 para este quede en secuencia
        last_order = (
            Lesson.objects
            .filter(course=course)
            .aggregate(Max('order'))
            ['order__max']
        )

        validated_data['order'] = (last_order or 0) + 1

        return super().create(validated_data)
    


class LessonUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = ['title', 'content']
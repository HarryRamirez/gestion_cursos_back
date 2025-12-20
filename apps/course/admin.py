from django.contrib import admin
from apps.course.models import Course, Category ,Lesson, LessonProgress, Enrollment, Review



admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(LessonProgress)
admin.site.register(Enrollment)
admin.site.register(Review)



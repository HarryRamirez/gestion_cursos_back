from django.urls import path
from .views import LessonProgressAPIView, LesssonProgressListAPIView



urlpatterns = [

    path('list/', LesssonProgressListAPIView.as_view()),
    path('lesson/<int:lesson_id>/progress/', LessonProgressAPIView.as_view(), name='lesson-progress'),
    

]




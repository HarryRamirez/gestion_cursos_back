from django.urls import path
from .views import CourseListAPIView, CourseCreateLessonAPIView, CourseListByIntructorAPIView



urlpatterns = [
    path('list/', CourseListAPIView.as_view()),
    path('list_by_instructor/', CourseListByIntructorAPIView.as_view()),
    path('create/', CourseCreateLessonAPIView.as_view()),
    
]
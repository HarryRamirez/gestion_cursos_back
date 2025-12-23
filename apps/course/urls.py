from django.urls import path
from .views import CourseListAPIView, CourseCreateLessonAPIView, CourseListByIntructorAPIView, CourseUpdateAPIView, CourseDeleteAPIView



urlpatterns = [
    path('list/', CourseListAPIView.as_view()),
    path('list_by_instructor/', CourseListByIntructorAPIView.as_view()),
    path('create/', CourseCreateLessonAPIView.as_view()),
    path('update/<int:pk>', CourseUpdateAPIView.as_view()),
    path('delete/<int:pk>', CourseDeleteAPIView.as_view()),
    
]
from django.urls import path
from .views import GetListLessonListAPIView, GetListLessonByInstructorListAPIView, PostLessonAPIView, UpdateLessonAPIView, DeleteLessonAPIView



urlpatterns = [
    path('list/', GetListLessonListAPIView.as_view()),
    path('list_by_instructor/', GetListLessonByInstructorListAPIView.as_view()),
    path('create/', PostLessonAPIView.as_view()),
    path('update/<int:pk>', UpdateLessonAPIView.as_view()),
    path('delete/<int:pk>', DeleteLessonAPIView.as_view()),
]
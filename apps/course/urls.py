from django.urls import path
from .views import CourseListAPIView



urlpatterns = [
    path('list/', CourseListAPIView.as_view()),
]
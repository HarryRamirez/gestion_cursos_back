from django.urls import path
from .views import EnrollmentListAPIView, InstructorEnrollmentListAPIView, EnrollmentCreateAPIView, EnrollmentUpdateAPIView



urlpatterns = [
    path('list/', EnrollmentListAPIView.as_view()),
    path('list_by_instructor/', InstructorEnrollmentListAPIView.as_view()),
    path('create/', EnrollmentCreateAPIView.as_view()),
    path('update/<int:pk>', EnrollmentUpdateAPIView.as_view()),
    
]
from django.urls import path
from .views import ReviewListAPIView, ReviewCreateAPIView, ReviewUpdateAPIView, ReviewDeleteAPIView



urlpatterns = [
    path('list/', ReviewListAPIView.as_view()),
    path('create/', ReviewCreateAPIView.as_view()),
    path('update/<int:pk>', ReviewUpdateAPIView.as_view()),
    path('delete/<int:pk>', ReviewDeleteAPIView.as_view()),
]
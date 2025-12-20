from django.urls import path
from .views import RegisterAPIView, ProfileView, ListsUserAPIView



urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('list_users/', ListsUserAPIView.as_view()),


]
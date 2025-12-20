from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsInstructor, IsAdminOrInstructor
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Course
from .serializers import GetListCourseSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q



class CoursePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    
class CourseListAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated, IsAdminOrInstructor]
    
    pagination_class = CoursePagination
    serializer_class = GetListCourseSerializer
    
    
    
    def get_queryset(self):
        
        queryset = Course.objects.filter(is_active=True, status='publicado')

        search_title = self.request.query_params.get('search_title')
        search_category = self.request.query_params.get('search_category')
        search_instructor = self.request.query_params.get('search_instructor')
        
        if search_title:
            queryset = queryset.filter(Q(title__icontains=search_title))
        if search_category:
            queryset = queryset.filter(Q(category__name__icontains=search_category))
        if search_instructor:
            for term in search_instructor.split():
                queryset = queryset.filter(
                    Q(instructor__first_name__icontains=term) | 
                    Q(instructor__last_name__icontains=term))
        
        queryset = queryset.order_by('created_at')

        return queryset
    
    
    def list(self, request, *args, **kwargs):
        pagination = request.query_params.get('paginate', 'true').lower()
        
        queryset = self.get_queryset()
        
        if pagination == 'false':
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'count': queryset.count(),
                'results': serializer.data
            })
            
        return super().list(queryset, *args, **kwargs)
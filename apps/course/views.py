from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Course
from .serializers import GetListCourseSerializer, PostCourseLessonsSerializer, UpdateCourseSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q



class CoursePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    
class CourseListAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
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
    
    

class CourseListByIntructorAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    pagination_class = CoursePagination
    serializer_class = GetListCourseSerializer
    
    
    
    def get_queryset(self):
        
        user = self.request.user
        
        queryset = Course.objects.filter(instructor=user, is_active=True)
        

        search_title = self.request.query_params.get('search_title')
        search_category = self.request.query_params.get('search_category')
        search_status = self.request.query_params.get('search_status')
        
        
        if search_title:
            queryset = queryset.filter(Q(title__icontains=search_title))
        if search_category:
            queryset = queryset.filter(Q(category__name__icontains=search_category))
        if search_status:
            queryset = queryset.filter(Q(status__icontains=search_status))
        
        
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




class CourseCreateLessonAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Course.objects.all()
    
    def post(self, request):
        
        serilalizer = PostCourseLessonsSerializer(data=request.data, context={'request': request})
        
        if serilalizer.is_valid():
            course = serilalizer.save()
            
            return Response(PostCourseLessonsSerializer(course).data, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serilalizer.errors}, status=status.HTTP_400_BAD_REQUEST)
        




class CourseUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Course.objects.all()
    
    def put(self, request, pk):
        
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'message': 'Curso no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateCourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    






class CourseDeleteAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Course.objects.all()
    
    
    def delete(self , request, pk):
    
        try:
            course = Course.objects.get(pk=pk, is_active=True)
        except Course.DoesNotExist:
            return Response({'message': 'curso no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        course.is_active=False
        course.save()
        
        return Response({'message': 'curso eliminado con exito'}, status=status.HTTP_204_NO_CONTENT)
        
        
    
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.course.models import Lesson
from .serializers import GetListLessonSerializer, PostLessonSerializer, UpdateLessonSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class PaginationLesson(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
    

class GetListLessonListAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    pagination_class = PaginationLesson
    serializer_class = GetListLessonSerializer
    
    
    
    def get_queryset(self):
        
        queryset = Lesson.objects.all().order_by('course')
        
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
            
        return super().list(request, *args, **kwargs)
        
        




class GetListLessonByInstructorListAPIView(ListAPIView):
    
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    pagination_class = PaginationLesson
    serializer_class = GetListLessonSerializer
    
    
    def get_queryset(self):
        
        user = self.request.user
        queryset = Lesson.objects.filter(course__instructor=user).order_by('course')
        
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
            
        return super().list(request, *args, **kwargs)
        
    
    


class PostLessonAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Lesson.objects.all()
    
    def post(self, request):
        
        serializer = PostLessonSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class UpdateLessonAPIView(APIView):
    
    def put(self, request, pk):
        
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({'message': 'leccion no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateLessonSerializer(lesson, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    



class DeleteLessonAPIView(APIView):
    
    def delete(self, request, pk):
        
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({'message': 'leccion no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        lesson.delete()
        return Response({'message': 'leccion eliminada correctamente'}, status=status.HTTP_200_OK)
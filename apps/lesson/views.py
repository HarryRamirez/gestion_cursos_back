from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.course.models import Lesson
from .serializers import LessonListSerializer, LessonCreateSerializer, LessonUpdateSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PaginationLesson(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
    

class GetListLessonListAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    pagination_class = PaginationLesson
    serializer_class = LessonListSerializer
    
    @swagger_auto_schema(
        operation_summary="Listar todas las lecciones",
        operation_description="""
        Retorna la lista completa de lecciones.
        La paginación puede desactivarse usando `paginate=false`.
        """,
        manual_parameters=[
            openapi.Parameter(
                'paginate',
                openapi.IN_QUERY,
                description="false para desactivar la paginación",
                type=openapi.TYPE_BOOLEAN,
                default=True
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Número de página",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Cantidad de elementos por página",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: LessonListSerializer(many=True),
            401: "No autenticado",
            403: "Sin permisos"
        },
        tags=["Lessons"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    
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
    serializer_class = LessonListSerializer
    

    @swagger_auto_schema(
        operation_summary="Listar lecciones del instructor",
        operation_description="Retorna las lecciones asociadas a cursos del instructor autenticado",
        manual_parameters=[
            openapi.Parameter(
                'paginate',
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                default=True
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: LessonListSerializer(many=True)},
        tags=["Lessons"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
      
    
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
    
    

    @swagger_auto_schema(
        operation_summary="Crear lección",
        operation_description="Crea una nueva lección",
        request_body=LessonCreateSerializer,
        responses={
            201: LessonCreateSerializer,
            400: "Datos inválidos",
            403: "Sin permisos"
        },
        tags=["Lessons"]
    ) 
    def post(self, request):
        
        serializer = LessonCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




class UpdateLessonAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Lesson.objects.all()
    
    
    @swagger_auto_schema(
        operation_summary="Actualizar lección",
        request_body=LessonUpdateSerializer,
        responses={
            200: LessonUpdateSerializer,
            404: "Lección no encontrada"
        },
        tags=["Lessons"]
    )
    def put(self, request, pk):
        
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({'message': 'leccion no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LessonUpdateSerializer(lesson, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    



class DeleteLessonAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Lesson.objects.all()

    
    
    @swagger_auto_schema(
        operation_summary="Eliminar lección",
        responses={
            200: "Lección eliminada correctamente",
            404: "Lección no encontrada"
        },
        tags=["Lessons"]
    )
    def delete(self, request, pk):
        
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({'message': 'leccion no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        lesson.delete()
        return Response({'message': 'leccion eliminada correctamente'}, status=status.HTTP_200_OK)
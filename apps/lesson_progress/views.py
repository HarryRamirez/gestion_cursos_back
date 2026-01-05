from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.course.models import Lesson, LessonProgress
from .serializers import LessonProgressSerializer, LessonProgressListSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

    
    
class LesssonProgressListAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = LessonProgress.objects.all()


    @swagger_auto_schema(
        operation_summary="Listar progreso de lecciones",
        operation_description="Retorna el progreso de todas las lecciones",
        responses={
            200: LessonProgressListSerializer(many=True),
            401: "No autenticado",
            403: "Sin permisos"
        },
        tags=["Lesson Progress"]
    )
    def get(self, request):
        
        lesson_progress = LessonProgress.objects.all()
        
        serializer = LessonProgressListSerializer(lesson_progress, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonProgressGetAPIView(APIView):
    
    def get(self, request, pk):
        pass
    
    
    
    
    
    
    
class LessonProgressAPIView(APIView):

    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = LessonProgress.objects.all()
    
    
    @swagger_auto_schema(
        operation_summary="Actualizar progreso de lección",
        operation_description="""
        Crea o actualiza el progreso de una lección
        para el estudiante autenticado.
        """,
        manual_parameters=[
            openapi.Parameter(
                'lesson_id',
                openapi.IN_PATH,
                description="ID de la lección",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=LessonProgressSerializer,
        responses={
            200: LessonProgressSerializer,
            400: "Datos inválidos",
            404: "Lección no encontrada"
        },
        tags=["Lesson Progress"]
    )
    def post(self, request, lesson_id):

        user = request.user
        lesson = get_object_or_404(Lesson, id=lesson_id)

        serializer = LessonProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson_progress, created = LessonProgress.objects.get_or_create(
            student=user,
            lesson=lesson
        )

        lesson_progress.progress = serializer.validated_data['progress']
        lesson_progress.completed = serializer.validated_data.get(
            'completed',
            lesson_progress.completed
        )

        lesson_progress.save()

        return Response(
            LessonProgressSerializer(lesson_progress).data,
            status=status.HTTP_200_OK
        )






from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.course.models import Enrollment
from .serializers import EnrollmentListSerializer, EnrollmentCreateSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class EnrollmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
    

class EnrollmentListAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    pagination_class = EnrollmentPagination
    serializer_class = EnrollmentListSerializer
    
    
    @swagger_auto_schema(
        operation_summary="Listar mis inscripciones",
        operation_description="""
        Retorna las inscripciones activas o completadas
        del estudiante autenticado.
        """,
        manual_parameters=[
            openapi.Parameter(
                'search_term',
                openapi.IN_QUERY,
                description="Buscar por nombre del curso",
                type=openapi.TYPE_STRING
            ),
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
                description="Cantidad de registros por página",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: EnrollmentListSerializer(many=True),
            401: "No autenticado",
            403: "Sin permisos"
        },
        tags=["Enrollments"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    
    def get_queryset(self):
        
        user = self.request.user
        queryset = Enrollment.objects.filter(
            student=user, 
            status__in=[Enrollment.STATUS_ACTIVE, Enrollment.STATUS_COMPLETED])
        
        search_term = self.request.query_params.get('search_term')
        
        if search_term:
            queryset = queryset.filter(Q(course__name__icontains=search_term))
        
        
        queryset = queryset.order_by('-enrolled_at')
        
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
    





class InstructorEnrollmentListAPIView(ListAPIView):
    
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    pagination_class = EnrollmentPagination
    serializer_class = EnrollmentListSerializer
    
    
    @swagger_auto_schema(
        operation_summary="Listar inscripciones de mis cursos",
        operation_description="""
        Retorna las inscripciones de los cursos
        del instructor autenticado.
        """,
        manual_parameters=[
            openapi.Parameter(
                'search_term',
                openapi.IN_QUERY,
                description="Buscar por curso",
                type=openapi.TYPE_STRING
            ),
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
        responses={200: EnrollmentListSerializer(many=True)},
        tags=["Enrollments"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    
    
    def get_queryset(self):
        user = self.request.user

        queryset = Enrollment.objects.filter(
            course__instructor=user
        )

        search_term = self.request.query_params.get('search_term')

        if search_term:
            queryset = queryset.filter(Q(course__name__icontains=search_term))

        return queryset.order_by('-enrolled_at')
    
    
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
    


    
    

class EnrollmentCreateAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Enrollment.objects.all()
    
    
    @swagger_auto_schema(
        operation_summary="Inscribirse en un curso",
        operation_description="""
        Crea una nueva inscripción.
        Si la inscripción existe y estaba cancelada,
        se reactiva automáticamente.
        """,
        request_body=EnrollmentCreateSerializer,
        responses={
            201: EnrollmentListSerializer,
            200: EnrollmentListSerializer,
            400: "Inscripción inválida",
            403: "Sin permisos"
        },
        tags=["Enrollments"]
    )
    def post(self, request):
        
        serializer = EnrollmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = serializer.validated_data['student']
        course = serializer.validated_data['course']

        enrollment = Enrollment.objects.filter(
            student=student,
            course=course
        ).first()

        if not enrollment:
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
                status=Enrollment.STATUS_ACTIVE
            )
            return Response(
                EnrollmentListSerializer(enrollment).data,
                status=status.HTTP_201_CREATED
            )

        if enrollment.status == Enrollment.STATUS_CANCELLED:
            enrollment.status = Enrollment.STATUS_ACTIVE
            enrollment.save(update_fields=['status'])
            return Response(
                EnrollmentListSerializer(enrollment).data,
                status=status.HTTP_200_OK
            )

        if enrollment.status == Enrollment.STATUS_ACTIVE:
            return Response(
                {'message': 'Ya estás inscrito en este curso'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'message': 'Este curso ya fue completado'},
            status=status.HTTP_400_BAD_REQUEST
        )
    







class EnrollmentUpdateAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Enrollment.objects.all()
    
    
    
    @swagger_auto_schema(
        operation_summary="Actualizar estado de inscripción",
        operation_description="""
        Permite cambiar el estado de una inscripción
        a ACTIVE, COMPLETED o CANCELLED.
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['status'],
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[
                        Enrollment.STATUS_ACTIVE,
                        Enrollment.STATUS_COMPLETED,
                        Enrollment.STATUS_CANCELLED
                    ]
                )
            }
        ),
        responses={
            200: "Estado actualizado",
            400: "Estado inválido",
            404: "Inscripción no encontrada"
        },
        tags=["Enrollments"]
    )
    def patch(self, request, pk):
        
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'message': 'El campo status es obligatorio'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in [
            Enrollment.STATUS_ACTIVE,
            Enrollment.STATUS_COMPLETED,
            Enrollment.STATUS_CANCELLED
        ]:
            return Response(
                {'message': 'Estado no válido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            enrollment = Enrollment.objects.get(
                pk=pk, status__in=[Enrollment.STATUS_ACTIVE, Enrollment.STATUS_COMPLETED])
        except Enrollment.DoesNotExist:
            return Response({'message': 'Inscripcion no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        
        enrollment.status = new_status
        enrollment.save()
        
        return Response({'message': 'Inscripcion cancelada'}, status=status.HTTP_200_OK)
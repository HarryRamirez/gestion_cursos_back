from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.course.models import Review
from .serializers import ReviewListSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class ReviewPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    
    
    
class ReviewListAPIView(ListAPIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    pagination_class = ReviewPagination
    serializer_class = ReviewListSerializer
    

    @swagger_auto_schema(
        operation_summary="Listar reviews",
        operation_description="""
        Retorna la lista de reviews registradas.
        
        - Soporta paginación por defecto.
        - Permite desactivar paginación usando `paginate=false`.
        - Permite filtrar por fecha de creación usando `search_term`.
        """,
        manual_parameters=[
            openapi.Parameter(
                name='search_term',
                in_=openapi.IN_QUERY,
                description='Filtrar reviews por fecha de creación (YYYY-MM-DD)',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='paginate',
                in_=openapi.IN_QUERY,
                description='Habilitar o deshabilitar paginación (true | false)',
                type=openapi.TYPE_STRING,
                required=False,
                default='true'
            ),
        ],
        responses={
            status.HTTP_200_OK: ReviewListSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: 'No autenticado',
            status.HTTP_403_FORBIDDEN: 'Sin permisos'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    


    def get_queryset(self):
        queryset = Review.objects.all().order_by('-created_at')
        
        search_term = self.request.query_params.get('search_term')
        
        if search_term:
            queryset = queryset.filter(Q(created_at=search_term))
        
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






class ReviewCreateAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Review.objects.all()

    @swagger_auto_schema(
        operation_summary="Crear una review",
        operation_description="""
        Permite a un estudiante crear una nueva review.
        
        - El estudiante se asigna automáticamente desde el usuario autenticado.
        """,
        request_body=ReviewCreateSerializer,
        responses={
            status.HTTP_201_CREATED: ReviewListSerializer,
            status.HTTP_400_BAD_REQUEST: 'Datos inválidos',
            status.HTTP_401_UNAUTHORIZED: 'No autenticado'
        }
    )
    def post(self, request):
        
        serializer = ReviewCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            
            review = serializer.save(student=request.user)
            return Response(ReviewListSerializer(review).data, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class ReviewUpdateAPIView(APIView):
   
   
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Review.objects.all()

    @swagger_auto_schema(
        operation_summary="Actualizar una review",
        operation_description="""
        Permite actualizar una review existente.
        
        - Solo el usuario que creó la review puede editarla.
        """,
        request_body=ReviewUpdateSerializer,
        responses={
            status.HTTP_200_OK: ReviewListSerializer,
            status.HTTP_400_BAD_REQUEST: 'Datos inválidos',
            status.HTTP_403_FORBIDDEN: 'No tienes permiso para editar esta review',
            status.HTTP_404_NOT_FOUND: 'Review no encontrada'
        }
    )
    def patch(self, request, pk):
        review = get_object_or_404(Review, id=pk)

        if review.student != request.user:
            return Response(
                {'detail': 'No tienes permiso para editar esta review'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ReviewUpdateSerializer(review, data=request.data)

        if serializer.is_valid():
            review = serializer.save()
            return Response(ReviewListSerializer(review).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ReviewDeleteAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Review.objects.all()
    
    @swagger_auto_schema(
        operation_summary="Eliminar una review",
        operation_description="""
        Elimina una review existente.
        
        - Solo el autor de la review puede eliminarla.
        """,
        responses={
            status.HTTP_204_NO_CONTENT: 'Review eliminado exitosamente',
            status.HTTP_403_FORBIDDEN: 'No tienes permiso para eliminar esta review',
            status.HTTP_404_NOT_FOUND: 'Review no encontrada'
        }
    )
    def delete(self, request, pk):

        review = get_object_or_404(Review, id=pk)

        if review.student != request.user:
            return Response(
                {'detail': 'No tienes permiso para eliminar esta review'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        review.delete()
        return Response({'message': 'Review eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)

        

from django.shortcuts import render
from apps.users.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, GetUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class ListsUserAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions] 
    

    @swagger_auto_schema(
        operation_summary="Listar usuarios",
        operation_description="Retorna la lista de usuarios activos",
        responses={200: GetUserSerializer(many=True)},
        tags=["Users"]
    )
    def get(self, request):
        
        user = User.objects.filter(is_active=True)
        
        serializer = GetUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        





class RegisterAPIView(APIView):
    
    permission_classes = [AllowAny] 

    @swagger_auto_schema(
        operation_summary="Registro de usuario",
        operation_description="Crea un nuevo usuario",
        request_body=RegisterSerializer,
        responses={
            201: GetUserSerializer,
            400: "Datos inválidos"
        },
        tags=["Auth"]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data = GetUserSerializer(user).data
            return Response(data, status=status.HTTP_201_CREATED)
        

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




## metodo del perfil del usuario autenticado
class ProfileView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Perfil del usuario",
        operation_description="Retorna la información del usuario autenticado",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'role': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        },
        tags=["Users"]
    )
    def get(self, request):
        return Response({
            "id": request.user.id,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "role": request.user.role.name
            
        })



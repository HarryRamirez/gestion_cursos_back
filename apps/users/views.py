from django.shortcuts import render
from apps.users.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, GetUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.views import APIView




class ListsUserAPIView(APIView):
    
    permission_classes = [IsAuthenticated, DjangoModelPermissions] 
    
    def get(self, request):
        
        user = User.objects.filter(is_active=True)
        
        serializer = GetUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        





class RegisterAPIView(APIView):
    
    permission_classes = [AllowAny] 
    
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

    def get(self, request):
        return Response({
            "id": request.user.id,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "role": request.user.role.name
            
        })



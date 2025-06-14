from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from .serializer import UserSerializer



def home(request):
       
    return Response(request,'ponto/home.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user is None or not user.check_password(password):
        return Response({'detail':'E-mail/Senha Invalido'},status=status.HTTP_400_BAD_REQUEST)

    token,_ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token':token.key,
        'username':user.username,
        'email':user.email,
        'cargo':user.profile.cargo
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        token,_ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": serializer.data,
            "email": user.email,
            "cargo":user.profile.cargo,             
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
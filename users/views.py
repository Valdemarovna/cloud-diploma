from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User

@api_view(['POST'])
def register(request):
    data = request.data

    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'User exists'}, status=400)

    user = User.objects.create_user(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        full_name=data['full_name'],
        storage_path=f"user_{data['username']}"
    )

    return Response({'message': 'User created'})


@api_view(['POST'])
def login_view(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )

    if user:
        login(request, user)
        return Response({'message': 'Logged in'})

    return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out'})


@api_view(['GET'])
def users_list(request):
    if not request.user.is_authenticated:
        return Response(status=401)

    users = User.objects.all().values()
    return Response(list(users))


@api_view(['DELETE'])
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return Response(status=403)

    User.objects.filter(id=user_id).delete()
    return Response({'message': 'Deleted'})

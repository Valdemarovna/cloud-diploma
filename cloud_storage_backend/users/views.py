from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created"}, status=201)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_view(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )

    if user:
        login(request, user)
        return Response({"message": "Logged in"})
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message": "Logged out"})

@api_view(['GET'])
def users_list(request):
    if not (request.user.is_admin or request.user.is_superuser):
        return Response({"error": "Forbidden"}, status=403)

    users = User.objects.all().values()
    return Response(list(users))

@api_view(['DELETE'])
def delete_user(request, user_id):
    if not (request.user.is_admin or request.user.is_superuser):
        return Response({"error": "Forbidden"}, status=403)

    User.objects.filter(id=user_id).delete()
    return Response({"message": "Deleted"})
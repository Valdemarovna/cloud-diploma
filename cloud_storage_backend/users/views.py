from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

def csrf(request):
    return JsonResponse({"message": "CSRF set"})

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        logger.info(f"User {request.data['username']} created")
        return Response({"message": "User created"}, status=201)

    logger.warning(f"Can not create User {request.data['username']}. Reason: {serializer.errors}")
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_view(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )

    if user:
        login(request, user)
        logger.info(f"User {request.data['username']} logged in")
        return Response({"message": "Logged in"})
    logger.warning(f"Invalid credentials for user {request.data['username']}")
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    logger.info(f"User {request.user} logged out")
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
    logger.info(f"User id {user_id} Deleted")
    return Response({"message": "Deleted"})

@api_view(['PATCH'])
def make_admin(request, user_id):
    if not (request.user.is_admin or request.user.is_superuser):
        return Response({"error": "Forbidden"}, status=403)

    try:
        user = User.objects.get(id=user_id)
        user.is_admin = True
        user.save()
        logger.info(f"User {user.username} is now admin")
        return Response({"message": "User is now admin"})
    except User.DoesNotExist:
        logger.error(f"User {user_id} Not found")
        return Response({"error": "Not found"}, status=404)

@api_view(['PATCH'])
def remove_admin(request, user_id):
    if not (request.user.is_admin or request.user.is_superuser):
        return Response({"error": "Forbidden"}, status=403)

    try:
        user = User.objects.get(id=user_id)

        # нельзя снять админа с самого себя
        if user == request.user:
            logger.warning(f"Cannot remove admin from yourself")
            return Response({"error": "Cannot remove admin from yourself"}, status=400)

        user.is_admin = False
        user.save()

        logger.info(f"Admin rights removed from User {user.username}")
        return Response({"message": "Admin rights removed"})

    except User.DoesNotExist:
        logger.error(f"User {user_id} Not found")
        return Response({"error": "Not found"}, status=404)
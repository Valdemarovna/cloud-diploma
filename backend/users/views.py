from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .validators import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        data = request.data

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        full_name = data.get("full_name")

        if not all([username, password, email, full_name]):
            return Response(
                {"error": "Все поля обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Логин уже занят"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email уже используется"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User(
            username=username,
            email=email,
            full_name=full_name
        )

        try:
            user.full_clean()  # 🔥 проверка валидаторов модели
        except ValidationError as e:
            return Response(
                {"error": e.message_dict},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()

        return Response(
            {"message": "Пользователь создан"},
            status=status.HTTP_201_CREATED
        )
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Введите логин и пароль"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Неверный логин или пароль"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)  # 🔥 создаёт сессию

        return Response({
            "message": "Успешный вход",
            "user": {
                "username": user.username,
                "is_admin": user.is_superuser
            }
        })
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Вы вышли из системы"})
    
class UsersListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Не авторизован"}, status=401)

        if not request.user.is_superuser:
            return Response({"error": "Нет прав"}, status=403)

        users = User.objects.all()

        data = []
        for user in users:
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_admin": user.is_superuser
            })

        return Response(data)
    
class DeleteUserView(APIView):
    def delete(self, request, user_id):
        if not request.user.is_authenticated:
            return Response({"error": "Не авторизован"}, status=401)

        if not request.user.is_superuser:
            return Response({"error": "Нет прав"}, status=403)

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "Пользователь удалён"})
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=404)
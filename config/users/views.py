from django.shortcuts import render
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

@api_view(['POST'])
def register(request):
    data = request.data

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    # Валидация
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', username):
        return Response({'error': 'Invalid username'}, status=400)

    if len(password) < 6:
        return Response({'error': 'Weak password'}, status=400)

    user = User.objects.create(
        username=username,
        email=email,
        full_name=full_name,
        password=make_password(password)
    )

    return Response({'message': 'User created'})

def login_view(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )

    if user:
        login(request, user)
        return Response({'message': 'OK'})
    return Response({'error': 'Invalid credentials'}, status=401)

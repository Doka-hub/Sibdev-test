from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .serializers import RegisterSerializer


@extend_schema(
    tags=['Users'],
    summary='Регистрация и активация пользователя',
)
class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


@extend_schema(
    tags=['Users'],
    summary='Получение токена аутентификации по email и password',
)
class TokenObtainPairView(TokenObtainPairView):
    pass

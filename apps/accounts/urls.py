from django.urls import path

from .views import RegisterAPIView, TokenObtainPairView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
]

from django.shortcuts import render
from rest_framework.views import APIView

from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, permissions
from .models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

class AccountsView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfileView(generics.RetrieveAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

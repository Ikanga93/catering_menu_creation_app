from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, serializers
from .models import Menu
from .serializers import MenuSerializer, UserRegistrationSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

# Homepage view

def home(request):
    return HttpResponse("<h1>Welcome to the Catering Management App</h1>")

# MenuViewSet
class MenuViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Menu.
    """
    queryset = Menu.objects.all().order_by('-created_at')
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(caterer=self.request.user)

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


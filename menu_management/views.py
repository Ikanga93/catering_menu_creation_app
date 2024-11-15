# menu_management/views.py
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Menu
from .serializers import MenuSerializer, UserRegistrationSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

# Homepage API view
class HomeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Catering Management App"})
   
class IsCaterer(permissions.BasePermission):
    """
    Custom permission to only allow caterers to create menus.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'caterer'
        )

# MenuViewSet
class MenuViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Menu.
    """
    queryset = Menu.objects.all().order_by('-created_at')
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsCaterer]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(caterer=self.request.user)

# UserViewSet
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# User Registration View (API)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

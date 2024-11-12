from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.permissions import AllowAny
from .models import Menu
from .serializers import MenuSerializer, UserRegistrationSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

# Homepage view

def home(request):
    return HttpResponse("<h1>Welcome to the Catering Management App</h1>")

class IsCaterer(permissions.BasePermission):
    """
    Custom permission to only allow caterers to create menus.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'caterer'
    
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

# User Registration View
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

'''
Explanation:

Profile Model: Extends the User model to include a role field.
Signals: Automatically create and update the Profile whenever a User is created or saved.
IsCaterer Permission: Custom permission that only allows users with the "caterer" role to create menus.
MenuViewSet: Overrides get_permissions to apply IsCaterer permission to the create action.
Assign Roles:

After user registration, assign roles via Django admin or extend the registration endpoint to include role selection.
'''


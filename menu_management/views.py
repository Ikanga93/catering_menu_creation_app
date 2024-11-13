from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Menu
from .forms import MenuForm  # Ensure MenuForm is defined in forms.py
from .serializers import MenuSerializer, UserRegistrationSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Homepage view

def home(request):
    return render(request, 'menu_management/home.html')  # Use a template for better UI

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
'''
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
'''
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

def register_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('menu_list')
        else:
            form = UserCreationForm()
        return render(request, 'menu_management/register.html', {'form': form})

def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('menu_list')
        else:
            form = AuthenticationForm()
        return render(request, 'menu_management/login.html', {'form': form})

def logout_view(request):
        logout(request)
        return redirect('login')

# @login_required
def menu_list_view(request):
# Fetch menus from the database
    if request.user.is_authenticated:
        menus = Menu.objects.filter(caterer=request.user)
    else:
        menus = []
    return render(request, 'menu_management/menu_list.html', {'menus': menus})

# Create Menu View
@login_required
def create_menu_view(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.caterer = request.user
            menu.save()
            return redirect('web:menu_list')  # Use namespaced URL
    else:
        form = MenuForm()
    return render(request, 'menu_management/create_menu.html', {'form': form})

# Delete Menu View
@login_required
def delete_menu_view(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id, caterer=request.user)
        menu.delete()
        return redirect('web:menu_list')  # Use namespaced URL
    except Menu.DoesNotExist:
        return HttpResponse("Menu not found or you don't have permission to delete it.", status=404)
'''
Explanation:

Profile Model: Extends the User model to include a role field.
Signals: Automatically create and update the Profile whenever a User is created or saved.
IsCaterer Permission: Custom permission that only allows users with the "caterer" role to create menus.
MenuViewSet: Overrides get_permissions to apply IsCaterer permission to the create action.
Assign Roles:

After user registration, assign roles via Django admin or extend the registration endpoint to include role selection.
'''


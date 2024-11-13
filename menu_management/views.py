# menu_management/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from .models import Menu
from .serializers import MenuSerializer, UserRegistrationSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import MenuForm  # Ensure you have a MenuForm defined in forms.py

# Homepage view
def home(request):
    return render(request, 'menu_management/home.html')  # Use template for better UI

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

# Standalone View Functions
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('web:home')  # Use namespace
    else:
        form = UserCreationForm()
    return render(request, 'menu_management/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('web:home')  # Use namespace
    else:
        form = AuthenticationForm()
    return render(request, 'menu_management/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('web:login')  # Use namespace

def menu_list_view(request):
    # Fetch menus from the database
    if request.user.is_authenticated:
        menus = Menu.objects.filter(caterer=request.user)
    else:
        menus = []
    return render(request, 'menu_management/menu_list.html', {'menus': menus})

def create_menu_view(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.caterer = request.user
            menu.save()
            return redirect('web:menu_list')  # Use namespace
    else:
        form = MenuForm()
    return render(request, 'menu_management/create_menu.html', {'form': form})

def delete_menu_view(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id, caterer=request.user)
        menu.delete()
        return redirect('web:menu_list')  # Use namespace
    except Menu.DoesNotExist:
        return HttpResponse("Menu not found or you don't have permission to delete it.", status=404)

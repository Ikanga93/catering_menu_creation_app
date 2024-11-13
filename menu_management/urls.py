# menu_management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, UserRegistrationView
from . import views

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('register/', views.register_view, name='register'),  # Web registration
    path('login/', views.login_view, name='login'),  # User login
    path('logout/', views.logout_view, name='logout'),  # User logout
    path('menus/', views.menu_list_view, name='menu_list'),  # Menu list view
    path('menus/create/', views.create_menu_view, name='create_menu'),  # Create menu
    path('menus/delete/<int:menu_id>/', views.delete_menu_view, name='delete_menu'),  # Delete menu
]

# menu_management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, UserRegistrationView
from . import views

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menus/', views.menu_list_view, name='menu_list'),
]

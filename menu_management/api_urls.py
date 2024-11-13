# menu_management/api_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, UserRegistrationView, UserViewSet

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # API routes for Menus and Users
    path('register/', UserRegistrationView.as_view(), name='api-register'),  # API registration
]


'''
Explanation:

API Routes: Registered under 'api/' in the project-level urls.py.
No Additional 'api/' Prefix: Avoids routes like 'api/api/menus/'.
'''
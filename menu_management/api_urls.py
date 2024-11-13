# menu_management/api_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, UserRegistrationView, UserViewSet

app_name = 'api'  # Define the app_name for namespacing

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

'''
Explanation:

MenuViewSet and UserViewSet: Handled by DRF's router.
UserRegistrationView: Handles API-based user registration under 'api/register/'.
'''
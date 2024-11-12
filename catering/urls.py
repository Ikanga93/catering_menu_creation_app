"""
URL configuration for catering project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from menu_management import urls as menu_urls  # Assuming your app is named 'menu_management'
from menu_management import views as menu_views  # Import the view

urlpatterns = [
    path('', menu_views.home, name='home'), # Homepage route
    path('admin/', admin.site.urls),
    path('api/', include(menu_urls)),  # Include your app's URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

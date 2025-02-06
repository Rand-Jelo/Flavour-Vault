"""
URL configuration for flavourvault project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import home_page

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Include frontend URLs (Home, Recipes, Account)
    path('', include('recipes.urls', namespace='recipes')),
    path('', home_page, name='home'),

    # API Routes (Separate from frontend)
    path('api/', include('recipes.api_urls', namespace='api')),

    # Authentication (dj-rest-auth & allauth)
    path('auth/', include('dj_rest_auth.urls')),  # Login, Logout, Password Change
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Signup
    path('accounts/', include('allauth.urls')),  # Django-allauth for email verification, password reset
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
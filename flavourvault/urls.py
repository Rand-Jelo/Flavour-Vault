from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Include frontend URLs (Home, Recipes, Account)
    path('', include('recipes.urls', namespace='recipes')),  # Only include recipes.urls

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
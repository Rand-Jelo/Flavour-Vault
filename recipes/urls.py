from django.urls import path, include
from .views import (
    home_page, recipes_page, recipe_detail_page, account_page, 
    create_recipe, delete_recipe  # Added delete_recipe import
)
from .auth_views import user_profile, delete_user

app_name = "recipes"

urlpatterns = [
    # Frontend Pages
    path('', home_page, name='home_page'),
    path('recipes/', recipes_page, name='recipes_page'),
    path('recipes/<int:recipe_id>/', recipe_detail_page, name='recipe_detail_page'),
    path('account/', account_page, name='account_page'),
    path('recipes/create/', create_recipe, name='create_recipe'),  

    # Recipe Deletion Endpoint (Fixing missing delete route)
    path('recipes/delete/<int:recipe_id>/', delete_recipe, name='delete_recipe'),

    # User Profile Endpoints
    path('user/profile/', user_profile, name='user-profile'),
    path('user/delete/', delete_user, name='delete-user'),

    # Include API Routes
    path('api/', include('recipes.api_urls', namespace='api')),
]
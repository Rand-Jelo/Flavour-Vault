from django.urls import path
from .views import (
    recipe_list, recipe_detail, signup_page, login_page, 
    home_page, recipes_page, recipe_detail_page, add_review, get_reviews, account_page, delete_recipe, create_recipe
)
from .auth_views import signup, login

urlpatterns = [
    # Frontend Pages
    path('', home_page, name='home_page'),
    path('signup/', signup_page, name='signup_page'),
    path('login/', login_page, name='login_page'),
    path('recipes/', recipes_page, name='recipes_page'),
    path('recipes/<int:id>/', recipe_detail_page, name='recipe_detail_page'),
    path('account/', account_page, name='account_page'),

    # API Endpoints (Authentication)
    path('api/auth/signup/', signup, name='signup'),
    path('api/auth/login/', login, name='login'),

    # API Endpoints (Recipes & Reviews)
    path('api/recipes/', recipe_list, name='recipe_list'),
    path('api/recipes/<int:id>/', recipe_detail, name='recipe_detail'),
    path('api/recipes/<int:recipe_id>/add_review/', add_review, name='add_review'),
    path('api/recipes/<int:recipe_id>/get_reviews/', get_reviews, name='get_reviews'),

    # Recipe Actions
    path('recipes/<int:recipe_id>/delete/', delete_recipe, name='delete_recipe'),
    path('recipes/create/', create_recipe, name='create_recipe'),
]

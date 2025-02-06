from django.urls import path
from .views import (
    recipe_list, recipe_detail_page, add_review, get_reviews,
    delete_recipe, create_recipe
)

app_name = "api" 

urlpatterns = [
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', recipe_detail_page, name='recipe_detail'),
    path('recipes/<int:recipe_id>/reviews/', get_reviews, name='get_reviews'),
    path('recipes/<int:recipe_id>/add_review/', add_review, name='add_review'),
    path('recipes/<int:recipe_id>/delete/', delete_recipe, name='delete_recipe'),
    path('recipes/create/', create_recipe, name='create_recipe'),
]
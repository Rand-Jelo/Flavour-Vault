from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Home page route
    path('', views.home_page, name='home'), 

    # Other recipe-related routes
    path('recipes/', views.recipes_page, name='recipes_page'),
    path('recipes/<int:recipe_id>/', views.recipe_detail_page, name='recipe_detail_page'),
    path('account/', views.account_page, name='account_page'),
    path('recipes/create/', views.create_recipe, name='create_recipe'),
    path('recipes/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('recipes/delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),

    # Add Review route
    path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'),
    # Delete Review route
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),

]
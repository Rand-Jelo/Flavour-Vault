from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Recipe, RecipeIngredient, Review
from .forms import RecipeForm, RecipeIngredientForm
from .serializers import RecipeSerializer, ReviewSerializer

# HOME PAGE VIEW
def home_page(request):
    """Render homepage with featured recipes."""
    featured_recipes = Recipe.objects.order_by('-created_at')[:6]  # Get latest 6 recipes
    return render(request, "home.html", {"featured_recipes": featured_recipes})

# RECIPE PAGE VIEW (List all recipes)
def recipes_page(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes.html", {"recipes": recipes})

# RECIPE DETAIL PAGE VIEW
def recipe_detail_page(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = recipe.reviews.all()
    return render(request, "recipe_detail.html", {"recipe": recipe, "reviews": reviews})

# ACCOUNT PAGE VIEW (Fixed)
@login_required
def account_page(request):
    """Display user's recipes and reviews."""
    user_recipes = Recipe.objects.filter(author=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    return render(request, "account.html", {
        "user": request.user,
        "user_recipes": user_recipes,
        "user_reviews": user_reviews
    })

# GET & POST RECIPES
@api_view(['GET', 'POST'])
def recipe_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Ensure the author is set
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET A SINGLE RECIPE
@api_view(['GET'])
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)

# ADD A REVIEW (Requires Authentication)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def add_review(request, recipe_id):
    """Handles adding a review to a recipe"""
    recipe = get_object_or_404(Recipe, id=recipe_id)

    serializer = ReviewSerializer(data=request.data, context={'request': request, 'recipe_id': recipe_id})
    if serializer.is_valid():
        serializer.save(user=request.user, recipe=recipe)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET REVIEWS FOR A SPECIFIC RECIPE
@api_view(['GET'])
def get_reviews(request, recipe_id):
    """Retrieve all reviews for a specific recipe"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = recipe.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# CREATE RECIPE (API-Based)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_recipe(request):
    """API to create a new recipe."""
    recipe_form = RecipeForm(request.data)
    
    if recipe_form.is_valid():
        recipe = recipe_form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        
        return Response({"message": "Recipe created successfully"}, status=status.HTTP_201_CREATED)
    
    return Response(recipe_form.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE RECIPE (API-Based)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_recipe(request, recipe_id):
    """API to delete a recipe owned by the authenticated user."""
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    recipe.delete()
    return Response({"message": "Recipe deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
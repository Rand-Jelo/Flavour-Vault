from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Recipe, Review
from .serializers import RecipeSerializer, ReviewSerializer

# HOME PAGE VIEW
def home_page(request):
    return render(request, "home.html")

# SIGNUP PAGE VIEW
def signup_page(request):
    return render(request, "signup.html")

# LOGIN PAGE VIEW
def login_page(request):
    return render(request, "login.html")

# RECIPE PAGE VIEW (List all recipes)
def recipes_page(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes.html", {"recipes": recipes})

# RECIPE DETAIL PAGE VIEW
def recipe_detail_page(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    reviews = recipe.reviews.all()
    return render(request, "recipe_detail.html", {"recipe": recipe, "reviews": reviews})

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
            serializer.save()
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

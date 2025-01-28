from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from .serializers import RecipeSerializer


# Create your views here.

# Homepage view
def home_page(request):
    return render(request, "home.html")

# Sign up page view
def signup_page(request):
    return render(request, "signup.html")


# Log in page view
def login_page(request):
    return render(request, "login.html")


# Recipe Page
def recipes_page(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes.html", {"recipes": recipes})


# Recipe Detail Page
def recipe_detail_page(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, "recipe_detail.html", {"recipe": recipe})


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

@api_view(['GET'])
def recipe_detail(request, id):
    try:
        recipe = Recipe.objects.get(pk=id)
    except Recipe.DoesNotExist:
        return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)


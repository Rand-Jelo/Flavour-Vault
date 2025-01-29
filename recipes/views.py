from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, RecipeIngredient, Review
from .forms import RecipeForm, RecipeIngredientForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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

# ACCOUNT PAGE VIEW
def account_page(request):
    return render(request, "account.html", {"user": request.user})

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


# ACCOUNT PAGE VIEW (For Logged-in User)
@login_required  # Ensures only logged-in users can access their account page
def account_page(request):
    user = request.user  # Get the logged-in user
    
    user_recipes = Recipe.objects.filter(author=user)  # Get recipes created by the user
    user_reviews = Review.objects.filter(user=user)  # Get reviews written by the user
    
    context = {
        "user": user,
        "user_recipes": user_recipes,
        "user_reviews": user_reviews,
    }
    return render(request, "account.html", context)


# Delete recipe
@login_required
def delete_recipe(request, recipe_id):
    """Allows users to delete their own recipes"""
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)  # Ensure user owns the recipe
    if request.method == 'POST':
        recipe.delete()  # Delete the recipe itself
        return redirect('account_page')  # Redirect to the account page after deleting

    return render(request, 'confirm_delete.html', {'recipe': recipe})


# Create Recipe
@login_required
def create_recipe(request):
    """Allows users to create a new recipe."""
    if request.method == 'POST':
        # Create the recipe form
        recipe_form = RecipeForm(request.POST, request.FILES)
        
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)  # Don't save yet, we need to associate the user
            recipe.author = request.user  # Associate the user who created the recipe
            recipe.save()  # Save the recipe

            # Handle ingredients form if there are ingredients selected
            ingredients = request.POST.getlist('ingredients')  # Get the selected ingredients
            quantities = request.POST.getlist('quantities')  # Get the quantities of the ingredients

            for ingredient, quantity in zip(ingredients, quantities):
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient_id=ingredient,
                    quantity=quantity
                )

            return redirect('recipes_page')  # Redirect to the recipes page after creating a new recipe

    else:
        recipe_form = RecipeForm()
        ingredient_form = RecipeIngredientForm()

    return render(request, "create_recipe.html", {
        "recipe_form": recipe_form,
        "ingredient_form": ingredient_form
    })

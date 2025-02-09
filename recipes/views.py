from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Recipe, RecipeIngredient, Review
from .forms import RecipeForm, ReviewForm
from .serializers import RecipeSerializer, ReviewSerializer
import json

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
    # Get the recipe details
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)  # Fetch linked ingredients
    reviews = recipe.reviews.all()

    # Initialize the duplicate_reviews flag
    duplicate_reviews = False

    # Check if the user is authenticated and has already posted a review for this recipe
    if request.user.is_authenticated and reviews.filter(user=request.user).exists():
        duplicate_reviews = True

    # Pass the flag to the template
    return render(request, "recipe_detail.html", {
        "recipe": recipe,
        "ingredients": ingredients,
        "reviews": reviews,
        "duplicate_reviews": duplicate_reviews  # Pass the flag to the template
    })

# ACCOUNT PAGE VIEW
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

# GET & POST RECIPES (API)
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

# GET A SINGLE RECIPE (API)
@api_view(['GET'])
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)

# ADD A REVIEW (API - Requires Authentication)
def add_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the user already has a review for this recipe
    existing_review = Review.objects.filter(user=request.user, recipe=recipe).first()
    
    if request.method == 'POST':
        if existing_review:
            # If the user has already posted a review, display an error message and return without saving
            messages.error(request, 'You have already submitted a review for this recipe.')
            return redirect(f"/recipes/{recipe.id}/")  # Redirect to prevent duplicate message

        else:
            # If no existing review, proceed to save the new one
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.recipe = recipe
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted successfully!')
                return redirect(f"/recipes/{recipe.id}/")  # Redirect to recipe detail page
    else:
        form = ReviewForm()

    return render(request, 'recipe_detail.html', {'recipe': recipe, 'form': form})

# GET REVIEWS FOR A SPECIFIC RECIPE (API)
@api_view(['GET'])
def get_reviews(request, recipe_id):
    """Retrieve all reviews for a specific recipe"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = recipe.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# CREATE RECIPE (Template-Based)
@login_required
def create_recipe(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredients_json = request.POST.get('ingredients_json')  # JSON string from hidden input

        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # Process ingredient JSON data
            if ingredients_json:
                try:
                    ingredients_data = json.loads(ingredients_json)
                    for ingredient in ingredients_data:
                        RecipeIngredient.objects.create(
                            recipe=recipe,
                            ingredient=ingredient["name"],
                            quantity=ingredient["quantity"],
                            unit=ingredient["unit"]
                        )
                except json.JSONDecodeError:
                    messages.error(request, "Error processing ingredients. Please try again.")

            return redirect('recipes:recipe_detail_page', recipe_id=recipe.id)

    else:
        recipe_form = RecipeForm()

    return render(request, "create_recipe.html", {'recipe_form': recipe_form})

# DELETE RECIPE
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def delete_recipe(request, recipe_id):
    """Delete a recipe owned by the authenticated user."""
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    recipe.delete()
    
    messages.success(request, "Recipe deleted successfully!")
    return redirect('recipes:account_page')

# EDIT RECIPE (Template-Based)
@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    if request.method == "POST":
        # Get the form and process ingredients
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredients_json = request.POST.get('ingredients_json')  # Get JSON data for ingredients

        if form.is_valid():
            form.save()

            # Handling ingredient update or creation
            if ingredients_json:
                try:
                    ingredients_data = json.loads(ingredients_json)

                    # Update existing ingredients
                    existing_ingredients = {ing.ingredient: ing for ing in RecipeIngredient.objects.filter(recipe=recipe)}
                    updated_ingredient_names = set()

                    for ingredient in ingredients_data:
                        ingredient_name = ingredient["name"].strip()
                        ingredient_quantity = ingredient["quantity"]
                        ingredient_unit = ingredient["unit"].strip()

                        if ingredient_name in existing_ingredients:
                            # Update existing ingredient
                            existing_ingredient = existing_ingredients[ingredient_name]
                            existing_ingredient.quantity = ingredient_quantity
                            existing_ingredient.unit = ingredient_unit
                            existing_ingredient.save()
                        else:
                            # Create new ingredient
                            RecipeIngredient.objects.create(
                                recipe=recipe,
                                ingredient=ingredient_name,
                                quantity=ingredient_quantity,
                                unit=ingredient_unit
                            )

                        updated_ingredient_names.add(ingredient_name)

                    # Remove ingredients that are no longer in the updated list
                    for ing_name in existing_ingredients.keys():
                        if ing_name not in updated_ingredient_names:
                            existing_ingredients[ing_name].delete()

                except json.JSONDecodeError:
                    messages.error(request, "Error processing ingredients. Please try again.")

            # Success message and redirect
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipes:recipe_detail_page', recipe_id=recipe.id)

    else:
        # Pre-fill the form with existing data
        form = RecipeForm(instance=recipe)

    # Render the edit recipe page with the form and ingredients
    return render(request, "edit_recipe.html", {
        "recipe": recipe,
        "form": form,
        "ingredients": ingredients
    })
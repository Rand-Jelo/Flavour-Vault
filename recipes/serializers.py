from rest_framework import serializers
from .models import Recipe, RecipeIngredient, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()  # Nested serializer to show ingredient details

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)  # Show ingredients

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'image', 'category', 'difficulty', 'created_at', 'ingredients']
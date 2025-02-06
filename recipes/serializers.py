from rest_framework import serializers
from .models import Recipe, RecipeIngredient, Ingredient, Review


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredients"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Serializer for Recipe Ingredients (Nested in Recipe)"""
    ingredient = IngredientSerializer() 

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Reviews, ensures users can only post one review per recipe"""
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'recipe', 'rating', 'content', 'created_at']
        extra_kwargs = {'recipe': {'read_only': True}} 

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """Prevent duplicate reviews"""
        request = self.context.get('request', None)
        recipe_id = self.context.get('recipe_id', None)

        if not request or not recipe_id:
            raise serializers.ValidationError("Request context or recipe ID is missing.")

        user = request.user

        # Check if user has already reviewed this recipe
        if Review.objects.filter(recipe_id=recipe_id, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this recipe.")

        validated_data['user'] = user
        validated_data['recipe'] = Recipe.objects.get(id=recipe_id)
        return super().create(validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipes with nested ingredients & reviews"""
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    ingredient_entries = serializers.ListField(write_only=True, required=False)  # Allow writing ingredients
    reviews = ReviewSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')  # Include recipe author

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions', 'image', 
            'category', 'difficulty', 'created_at', 'author',
            'ingredients', 'ingredient_entries', 'reviews'
        ]

    def create(self, validated_data):
        """Create a recipe with ingredients"""
        ingredient_entries = validated_data.pop('ingredient_entries', [])

        # Create the recipe
        recipe = Recipe.objects.create(**validated_data)

        # Add ingredients
        for entry in ingredient_entries:
            ingredient = Ingredient.objects.get_or_create(name=entry['name'])[0]
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=entry['quantity'])

        return recipe
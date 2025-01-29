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
        request = self.context['request']
        recipe_id = self.context['recipe_id']
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
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions', 'image', 
            'category', 'difficulty', 'created_at', 'ingredients', 'reviews'
        ]

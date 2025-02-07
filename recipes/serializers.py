from rest_framework import serializers
from .models import Recipe, RecipeIngredient, Review

class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Serializer for Recipe Ingredients (Now Uses Text Input for Ingredient Name)"""
    ingredient = serializers.CharField()  # Changed from ForeignKey to CharField

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']  # Ensure unit is included

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
    """Serializer for Recipes with text-based category and nested ingredients & reviews"""
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    ingredient_entries = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )  # Allow writing ingredients

    category = serializers.CharField()  # Changed from ForeignKey to CharField
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
        """Create a recipe with manually entered category and ingredients"""
        ingredient_entries = validated_data.pop('ingredient_entries', [])
        category = validated_data.pop('category', '').strip()  # Ensure category is saved as text

        # Create the recipe
        recipe = Recipe.objects.create(**validated_data, category=category)

        # Add ingredients
        for entry in ingredient_entries:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=entry['ingredient'],  # Now stored as text
                quantity=entry['quantity'],
                unit=entry['unit']
            )

        return recipe
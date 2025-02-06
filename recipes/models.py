from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()

# Food category for recipes
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    cuisine_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.cuisine_type}"

# Recipe model to store all recipes
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty = models.CharField(
        max_length=10, choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Ingredient model to store ingredients
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Model for linking recipes with ingredients
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.01'))]  # Corrected import
    )
    unit = models.CharField(max_length=20, default="grams") 

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name}"

# Model for user reviews on recipes
class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')  # Ensures a user can only review a recipe once

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} ({self.rating})"

# Model for user favorite recipes
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_favorite')
        ]

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"
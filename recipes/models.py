from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Food catagory for recipes
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


# Model to connect Ingredients and recipes
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)  # Example: "2 cups", "1 tbsp"

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.title}"


# Model for user reviews on recipes
class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} ({self.rating})"

# Model for user favorite recipes
class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"

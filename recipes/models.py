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
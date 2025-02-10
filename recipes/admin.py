from django.contrib import admin
from .models import Recipe, RecipeIngredient, Review

# Register your models here.


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # Allows adding at least one ingredient initially


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]

# Register models in Django Admin
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Review)
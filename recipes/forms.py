from django import forms
from .models import Recipe, RecipeIngredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'image', 'category', 'difficulty']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Enter quantity in grams'})
        }
from django import forms
from .models import Recipe, RecipeIngredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'image', 'category', 'difficulty']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter recipe description'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter instructions'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category'}),  # ✅ Changed from Select to TextInput
            'difficulty': forms.Select(choices=[
                ('Easy', 'Easy'),
                ('Medium', 'Medium'),
                ('Hard', 'Hard')
            ], attrs={'class': 'form-control'}),
        }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter quantity in grams'
            }),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., grams'})
        }
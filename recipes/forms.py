from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(
        max_length=255,
        label="Ingredients (separated by commas)",
        widget=forms.TextInput(attrs={"placeholder": "e.g. bread, cheese, butter"})
    )
    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
        label="Instructions (optional)"
    )
    cooking_time = forms.IntegerField(
        min_value=1,
        max_value=1440,
        label="Cooking Time (in minutes)",
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 3"})
    )
    name = forms.CharField(
        max_length=50,
        label="Recipe Name",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Grilled Cheese Sandwich"})
    )
    image = forms.ImageField(required=False, label="Recipe Image (optional)")
    class Meta:
        model = Recipe
        fields = ["name", "ingredients", "cooking_time", "instructions", "image"]
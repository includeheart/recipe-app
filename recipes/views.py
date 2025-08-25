from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def recipes(request):
    return render(request, 'recipes/recipes.html')

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes.html'
    context_object_name = 'recipes'
    login_url = 'login'

class RecipeInstructionsView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_instructions.html'
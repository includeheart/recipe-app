from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .forms import RecipeForm
from .models import Recipe

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

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            if any(f.name == "author" for f in Recipe._meta.get_fields()):
                recipe.author = request.user  # adjust field name if different
            if any(f.name == "user" for f in Recipe._meta.get_fields()):
                recipe.user = request.user
            recipe.save()
            return redirect("recipes:recipe-list")
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {"form": form})
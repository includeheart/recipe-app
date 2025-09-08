from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe-list"),
    path("list/<int:pk>/", views.RecipeInstructionsView.as_view(), name="recipe-instructions"),
    path("new/", views.recipe_create, name="recipe-create"),
]
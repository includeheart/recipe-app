from django.urls import path
from .views import RecipeListView, RecipeInstructionsView

app_name = 'recipes'

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe-list'),
    path('list/<int:pk>/', RecipeInstructionsView.as_view(), name='recipe-instructions'),
]
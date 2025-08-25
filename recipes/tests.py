from django.db import models
from django.test import TestCase

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    cooking_time = models.IntegerField()

    def return_ingredients_as_list(self):
        return [ingredient.strip() for ingredient in self.ingredients.split(',')]


    @property
    def difficulty(self):
        if self.cooking_time < 10:
            return 'easy'
        elif 10 <= self.cooking_time <= 30:
            return 'intermediate'
        else:
            return 'hard'

    def get_absolute_url(self):
        return f"/list/{self.id}/"


class RecipeModelTest(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="ingredient1, ingredient2",
            cooking_time=15
        )

    def test_return_ingredients_as_list(self):
        self.assertEqual(self.recipe.return_ingredients_as_list(), ["ingredient1", "ingredient2"])

    def test_calculate_difficulty(self):
        self.recipe.cooking_time = 5
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'easy')

        self.recipe.cooking_time = 15
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'intermediate')

    def test_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), '/list/1/')
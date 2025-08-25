from django.db import models
from django.urls import reverse

# Create your models here.
DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('intermediate', 'Intermediate'),
    ('hard', 'Hard'),
]

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.PositiveIntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, blank=True, editable=False)
    instructions = models.TextField(blank=True)
    image = models.ImageField(upload_to='Recipes', default='no_picture.jpg')
    def __str__(self):
        return str(self.name)
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return [i.strip() for i in self.ingredients.split(',') if i.strip()]
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10:
            self.difficulty = 'easy' if num_ingredients < 4 else 'medium'
        else:
            self.difficulty = 'intermediate' if num_ingredients < 4 else 'hard'
    def save(self, *args, **kwargs):
        self.calculate_difficulty()
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('recipes:recipe-instructions', kwargs={'pk': self.pk})
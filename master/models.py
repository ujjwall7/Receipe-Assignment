from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('creator', 'Creator'),
        ('viewer', 'Viewer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='viewer')

    def __str__(self):
        return f"{self.username} - {self.user_type}"

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='ingredient_images/')

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()
    prep_duration = models.IntegerField() 
    cook_duration = models.IntegerField() 
    step_by_step_pictures = models.ImageField(upload_to='recipe_steps/')
    thumbnail_image = models.ImageField(upload_to='thumbnails/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_recipes')

class Favourite(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

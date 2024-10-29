# serializers.py
from rest_framework import serializers
from .models import *

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']
        read_only_fields = ['user_type']

# Ingredient Serializer
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'image']

# Recipe Serializer
class RecipeSerializer(serializers.ModelSerializer):
    # ingredients = IngredientSerializer(many=True)
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions',
            'prep_duration', 'cook_duration', 'step_by_step_pictures', 'thumbnail_image', 'creator'
        ]

# Favourite Serializer
class FavouriteSerializer(serializers.ModelSerializer):
    recipe = serializers.ReadOnlyField(source='recipe.title')
    viewer = serializers.ReadOnlyField(source='viewer.username')

    class Meta:
        model = Favourite
        fields = ['id', 'recipe', 'viewer', 'marked_at']

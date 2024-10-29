from django.contrib import admin
from . models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active']
    list_filter = ['user_type', 'is_staff', 'is_active', 'date_joined']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']
    search_fields = ['name']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'prep_duration', 'cook_duration']
    list_filter = ['creator', 'prep_duration', 'cook_duration']
    search_fields = ['title', 'description']
    filter_horizontal = ['ingredients']

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'viewer', 'marked_at']
    list_filter = ['marked_at']
    search_fields = ['recipe__title', 'viewer__username']
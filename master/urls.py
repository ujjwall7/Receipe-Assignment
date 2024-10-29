# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('recipes/', RecipeView.as_view(), name='recipe-list-create'),
    path('recipes/favourite/', FavouriteRecipeView.as_view(), name='recipe-favourite'),
    path('ingredient/', IngredientView.as_view(), name='ingredient'),
    path('receipe-download-pdf/', RecipeDownloadView.as_view(), name='receipe-download'),
]

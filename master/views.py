from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.shortcuts import render

#PDF Genration 
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from django.shortcuts import render, redirect, HttpResponse


class RecipeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recipe_id = self.request.query_params.get('recipe_id')
        try:
            recipe = Recipe.objects.get(id = recipe_id)
            serializer = RecipeSerializer(recipe, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            recipes = Recipe.objects.all()
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.user_type != 'creator':
            return Response({'error': 'Only creators can create recipes.'}, status=status.HTTP_403_FORBIDDEN)
        get_ingredients_id = eval(request.data.get('ingredients',[]))
        ingredients = Ingredient.objects.filter(id__in = get_ingredients_id)
        print(ingredients)
        print(get_ingredients_id)
        print(type(get_ingredients_id))
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            ins = serializer.save(creator=request.user) 
            ins.ingredients.set(ingredients)           
            return Response({'msg': 'Receipe Created Successfully', 'success':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        recipe_id = self.request.query_params.get('recipe_id')
        try:
            recipe = Recipe.objects.get(id = recipe_id)
        except Exception as e:
            return Response({'error': f'{e}'})
        
        if request.user != recipe.creator:
            return Response({'error': 'Only the creator can edit this recipe.'}, status=status.HTTP_403_FORBIDDEN)

        get_ingredients_id = eval(request.data.get('ingredients',[]))
        ingredients = Ingredient.objects.filter(id__in = get_ingredients_id)

        serializer = RecipeSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            ins = serializer.save(creator=request.user) 
            ins.ingredients.set(ingredients)    
            return Response({'msg': 'Receipe Updated Successfully', 'success':True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        recipe_id = self.request.query_params.get('recipe_id')
        try:
            recipe = Recipe.objects.get(id = recipe_id)
        except Exception as e:
            return Response({'error': f'{e}'})
        
        if request.user != recipe.creator:
            return Response({'error': 'Only the creator can delete this recipe.'}, status=status.HTTP_403_FORBIDDEN)
        recipe.delete()
        return Response({'message': 'Recipe deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class FavouriteRecipeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        get_all_favourites = Favourite.objects.filter(viewer__id = user.id)
        serializer = FavouriteSerializer(get_all_favourites, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        recipe_id = self.request.query_params.get('recipe_id')
        if request.user.user_type != 'viewer':
            return Response({'error': 'Only viewers can mark recipes as favourite.'}, status=status.HTTP_403_FORBIDDEN)

        recipe = get_object_or_404(Recipe, id=recipe_id)
        favourite, created = Favourite.objects.get_or_create(recipe=recipe, viewer=request.user)

        if created:
            return Response({'message': 'Recipe added to favourites.'}, status=status.HTTP_201_CREATED)
        else:
            favourite.delete()
            return Response({'message': 'Recipe removed from favourites.'}, status=status.HTTP_204_NO_CONTENT)

class IngredientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'creator':
            return Response({'error': 'Only creators can view ingredient.'}, status=status.HTTP_403_FORBIDDEN)

        ingredient_id = request.query_params.get('ingredient_id')
        
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            ingredients = Ingredient.objects.all()
            serializer = IngredientSerializer(ingredients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.user_type != 'creator':
            return Response({'error': 'Only creators can create ingredient.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Ingredient Created Successfully', 'success':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if request.user.user_type != 'creator':
            return Response({'error': 'Only creators can update ingredient.'}, status=status.HTTP_403_FORBIDDEN)

        ingredient_id = request.query_params.get('ingredient_id')
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
        except Ingredient.DoesNotExist:
            return Response({'error': 'Ingredient not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = IngredientSerializer(ingredient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if request.user.user_type != 'creator':
            return Response({'error': 'Only delete can create ingredient.'}, status=status.HTTP_403_FORBIDDEN)

        ingredient_id = request.query_params.get('ingredient_id')
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
        except Ingredient.DoesNotExist:
            return Response({'error': 'Ingredient not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        ingredient.delete()
        return Response({'message': 'Ingredient deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class RecipeDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = self.request.query_params.get('recipe_id')
        try:
            recipe = Recipe.objects.get(id = id)
        except Exception as e:
            return Response({'error': f'{e}'})
        
        context = {'recipe':Recipe.objects.filter(id=id).last()}
        template_path = 'receipe.html'
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="receipe.pdf"'

        template = get_template(template_path)

        html = template.render(context)

        #Create PDF
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response



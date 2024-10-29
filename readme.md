Recipe Management System
This Recipe Management System has been developed using the Django Rest Framework. Its purpose is to enable users to create, view, update, delete, and favorite recipes.

Features
User Authentication: Users must register as either creators or viewers.
Recipe Management: Creators can create, update, and delete their recipes.
Favorite Recipes: Viewers can mark recipes as favorites or unmark them.
Ingredient Management: Creators can create, view, update, and delete ingredients.
PDF Generation: Users can download recipes in PDF format.
Installation
Clone the repository:

bash
Copy code
git clone <repository-url>
cd recipe-management-system
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run migrations:

bash
Copy code
python manage.py migrate
Create a superuser (optional):

bash
Copy code
python manage.py createsuperuser
Run the server:

bash
Copy code
python manage.py runserver
Access the API: Open your browser and navigate to http://127.0.0.1:8000/api/.

API Endpoints
Recipes
List/Create Recipes: GET /api/recipes/

Description: This endpoint displays a list of recipes or creates a new recipe.
Get Recipe: GET /api/recipes/?recipe_id=<recipe_id>

Description: Displays the details of a specific recipe.
Update Recipe: PUT /api/recipes/?recipe_id=<recipe_id>

Description: Updates a specific recipe.
Delete Recipe: DELETE /api/recipes/?recipe_id=<recipe_id>

Description: Deletes a specific recipe.
Favorite Recipes
List Favorite Recipes: GET /api/recipes/favourite/

Description: Displays a list of the user's favorite recipes.
Mark/Unmark Favorite Recipe: POST /api/recipes/favourite/?recipe_id=<recipe_id>

Description: Marks or unmarks a recipe as a favorite.
Ingredients
List/Create Ingredients: GET /api/ingredient/

Description: This endpoint displays a list of ingredients or creates a new ingredient.
Update Ingredient: PUT /api/ingredient/?ingredient_id=<ingredient_id>

Description: Updates a specific ingredient.
Delete Ingredient: DELETE /api/ingredient/?ingredient_id=<ingredient_id>

Description: Deletes a specific ingredient.
Recipe PDF Download
Download Recipe PDF: GET /api/receipe-download-pdf/?recipe_id=<recipe_id>
Description: Downloads the recipe in PDF format.
Models
User: For user authentication, with user types of either creator or viewer.
Ingredient: Holds details of ingredients.
Recipe: Contains details of recipes, their ingredients, and creator information.
Favourite: Records the user's favorite recipes.
Contributing
If you would like to contribute to this project, please submit a pull request. You may also report issues or suggest new features.

License
This project is licensed under the MIT License.


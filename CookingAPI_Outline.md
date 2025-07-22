Note: As of 7/20, this outline does not include Authorization/Security/Tokens. This will be incorporated at a later date.
## Database Structure

Main Principles: 
* Storing data in multiple databases is easier to handle and manage
	* ex. Easier to make one change in one database then a lot of changes across databases
* Essentially, that means having as many tables of different data as possible, and then using many-to-many relationships
* 4 main tables - users, recipes, ingredients, shopping lists - with 2 relational databases for recipes-ingredients and ingredients-shopping lists

**Database System**: PostgreSQL
* Was between this and SQLite
	* While SQLite is much easier to use, as a production quality/professional database it doesn't seem to have much utility
		* Storing a database in a file sounds wild, especially sounds bad for scaling
			* Only one reader/writer at a time, performance bottleneck in the future
##### Tables
###### Table 1: Users
**Purpose**: Store user information needed to run the program per user
**Fields:**
* user_id: Integer (Primary Key) - id of each user, increments itself + unique
* username : String(Required) - Username of the user, whatever they want
* password: String(Required) - Hashed password of the user, used to verify their login
**Relationships:** 
* One to many with recipes (a user can have multiple recipes, a recipe can only have one user)
###### Table 2: Recipes
**Purpose**: Store all the recipes created by all users.
**Fields**:
* recipe_id: Integer (Primary Key) - id for each recipe, increments+unique
* recipe_name: String (Required) - name of the recipe
* recipe_instructions: String (required) - instructions for cooking
* recipe_time: Integer (required) - Time required to complete the recipe from start to finish
* owner_id: Integer(required, ForeignKey) - maps each recipe to an owner in Users
**Relationships**: 
* One to many with users (a user can have many recipes, a recipe has one user)
* Many to many with ingredients (a recipe can have multiple ingredients, an ingredient can have multiple recipes)

###### Table 3: Ingredients
**Purpose**: Store all ingredients needed for all the recipes, needed for shopping list functionality
**Fields**:
* ingredient_id: Integer (Primary key) - id of each ingredient, increments + unique
* ingredient_name: String(required) - name of each ingredient
**Relationships**:
* Many to many with Recipes a recipe can have multiple ingredients, an ingredient can have multiple recipes)

**Table 4: Recipe_Ingredients_Mapping
**Purpose:** Facilitate the many to many relationship between ingredients and recipes
**Fields:**
* recipe_ingredient_id: Integer(Primary key) - id of each mapping, increments + unique
* recipe_id: Integer (Foreign Key) - recipe for the mapping
* ingredient_id: Integer (Foreign Key) - ingredient for the mapping
* quantity: Decimal(required) - amount of the ingredient
* unit: String(required) - units of measurement

###### Table 5: Shopping List
**Purpose**: Shopping List for each User
**Fields**:
* shopping_id: Integer (Primary key) - id of each shopping list, increments + unique
* shopping_name: String(required) - name of each ingredient
* owner_id: Integer(required, ForeignKey) - maps each shopping list to an owner in Users
**Relationships**:
* One to many with Users - each user can have multiple shopping lists
* Many to many with ingredients - a shopping lisgt has multiple ingredients, an ingredient can have multiple shopping lists

###### Table 6: Shopping List Items
**Purpose**: Facilitates the many to many relationship between shopping list and ingredients.
**Fields**:
* list_id: Integer (Primary key) - id of each list, increments + unique
* shopping_id: Integer(required, ForeignKey) - maps each list of items to an shopping list in the shopping list table
* ingredient_id: Integer(required, ForeignKey) - maps each shopping list to an ingredient in Ingredients
* quantity: Decimal(required) - amount of the ingredient
* unit: String(required) - units of measurement
* is_checked(default = False) - if the item is in the list
## API Structure

**General Methods:** - response will be the user/ingredient/recipe they are affecting, these will create/read/update/delete any of the tables and their mapping(for ingredients/recipes). Unsure if their will be a general version without a parameter.
1. GET /user{user_id}
2. GET /recipe{recipe_id}
3. GET /ingredient{ingredient_id}
4. GET /shopping_list{shopping_id}
5. POST /user{user_id}
6. POST /recipe{recipe_id}
7. POST /ingredient{ingredient_id}
8. POST /shopping_list{shopping_id}
9. PUT /user{user_id}
10. PUT /recipe{recipe_id}
11. PUT /ingredient{ingredient_id}
12. PUT /shopping_list{shopping_id}
13. DELETE /user{user_id}
14. DELETE /recipe{recipe_id}
15. DELETE /ingredient{ingredient_id}
16. DELETE /shopping_list{shopping_id}
**Specialized Methods:** These api endpoints are for specific features of the API
17. GET /recipe/search?ingredients=
	1. This is to return recipes for specific ingredients
	2. and/or version?
	3. Will return a list of recipe ids
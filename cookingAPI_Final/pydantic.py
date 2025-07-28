from pydantic import BaseModel, Field


'''
Outline:

User:
    userBaseModel(BaseModel) - username (string), password(string)
    userCreate(userBaseModel) - pass (same as userBase)
    userModel(userBaseModel) -userID (int)
    userUpdate(BaseModel) - username(string, optional), password(string, optional)
Recipe:
    recipeBaseModel(BaseModel) - name(string), instructions(string), time(int), owner_id(int)
    recipeCreate(recipeBaseModel) - ingredients(List of ints)
    recipeModel(recipeBaseModel) - recipeID(int)
    recipeUpdate(BaseModel) - name(string, optional), instructions(string, optional), time(int, optional) ingredients(List of ints, optional)
Ingredient:
    ingredientBaseModel(BaseModel) - name(string)
    ingredientCreate(ingredientBaseModel) - pass(same as base)
    ingredientModel(ingredientBaseModel) - ingredientID(int)
    ingredientUpdate(BaseModel) - name(string, optional)
ShoppingList:
    shoppingBaseModel(BaseModel) - name(string), ownerID(int)
    shoppingCreate(ingredientBaseModel) - pass(same as base)
    shoppingModel(ingredientBaseModel) - ingredients(List of IDs)
    shoppingUpdate(BaseModel) - name(string, optional)
RecipeIngredient:
    recipeIngredientBaseModel(BaseModel) - ingredient_id(int),quantity(float),unit(string)
    recipeIngredientCreate(recipeIngredientBaseModel) - pass(same as base)
    recipeIngredientModel(recipeIngredientBaseModel) - ingredientID(int)
    recipeIngredientUpdate(BaseModel) - quantity(optional, float), unit(string, optional)
shoppingIngredient:
    shoppingIngredientBaseModel(BaseModel) - ingredient_id(int), shoppingListID(int),quantity(float),unit(string), isChecked(boolean)
    shoppingIngredientCreate(shoppingIngredientBaseModel) - pass(same as base)
    shoppingIngredientModel(shoppingIngredientBaseModel) - shoppingingredientID(int)
    shoppingIngredientBaseModel(BaseModel) - ,quantity(float, optional),unit(string, optional), isChecked(boolean, optional)





'''
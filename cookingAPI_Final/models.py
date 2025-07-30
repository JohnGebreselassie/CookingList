from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class UnitEnum(str, Enum): #this exists to make units consistent across all namings - before, gram != Gram != g
    GRAM = "g"
    KILOGRAM = "kg"
    OUNCE = "oz"
    LITER = "l"
    CUP = "cup"
    TABLESPOON = "tbsp"
    TEASPOON = "tsp"
    PIECE = "piece"


#---------------------------------------RECIPE-INGREDIENT-----------------------------------------


class recipeIngredientBase(BaseModel): #base class
    ingredient_id: int = Field(..., gt=0, description = 'ingredient associated with this recipe')
    recipe_id: int = Field(..., gt=0, description="Recipe this ingredient is part of")
    quantity: float = Field(..., gt=0, description = 'amount of an ingredient')
    unit: UnitEnum = Field(..., description = "unit of measurement")

class recipeIngredientCreate(recipeIngredientBase): #create a recipe-ingredient mapping
    pass 

class recipeIngredientModel(recipeIngredientBase): #for when you need to return everything associated with a recipe-ingredient pair
    recipe_ingredient_id: int = Field(..., description = "unique id for a recipe_ingredient mapping")


class recipeIngredientUpdate(BaseModel): #optional parameters
    quantity: Optional[float] = Field(None, gt=0, description = 'amount of an ingredient')
    unit: Optional[UnitEnum] = Field(None, description = "unit of measurement")



#---------------------------------------SHOPPING-INGREDIENT-----------------------------------------


class shoppingIngredientBase(BaseModel): #base class
    ingredient_id: int = Field(..., gt=0, description = 'ingredient associated with this pairing')
    shopping_list_id: int = Field(..., gt=0, description = 'shopping_list associated with this pairing')
    quantity: float = Field(..., gt=0, description = 'amount of an ingredient')
    unit: UnitEnum = Field(..., description = "unit of measurement")
    isChecked: bool = Field(..., description= "whether the item is checked off the list")

class shoppingIngredientCreate(shoppingIngredientBase): #create a shopping_list-ingredient mapping
    pass

class shoppingIngredientModel(shoppingIngredientBase): #for when you need to return everything associated with a shopping_list-ingredient pair
    shopping_ingredient_id: int = Field(..., description = "unique id for a shopping_list-ingredient mapping")


class shoppingIngredientUpdate(BaseModel): #optional parameters
    quantity: Optional[float] = Field(None, gt=0, description = 'amount of an ingredient')
    unit: Optional[UnitEnum] = Field(None, description = "unit of measurement")
    isChecked: Optional[bool] = Field(None, description= "whether the item is checked off the list")



#---------------------------------------USER-----------------------------------------


class userBase(BaseModel): #base class
    username: str = Field(..., min_length=1, max_length=512, description = "username")
    password: str = Field(..., description = "password for user")

class userCreate(userBase): #create a user
    pass

class userModel(userBase): #for when you need to return everything associated with a user
    user_id: int = Field(..., description = "unique id for user instance")
    class Config:
        orm_mode = True
class userUpdate(BaseModel): #optional parameters
    username: Optional[str] = Field(None, min_length=1, max_length=512, description = "username")
    password: Optional[str] = Field(None, description = "password for user")



#---------------------------------------INGREDIENT-----------------------------------------


class ingredientBase(BaseModel): #base class
    ingredient_name: str = Field(..., min_length=1, max_length=512, description = "ingredient name")

class ingredientCreate(ingredientBase): #create a ingredient
    pass

class ingredientModel(ingredientBase): #for when you need to return everything associated with a ingredient
    ingredient_id: int = Field(..., description = "unique id for ingredient instance")

class ingredientUpdate(BaseModel): #optional parameters
    ingredient_name: Optional[str] = Field(None, min_length=1, max_length=512, description = "ingredient name")


#---------------------------------------RECIPE-----------------------------------------


class recipeBase(BaseModel): #base class
    recipe_name: str = Field(..., min_length=1, max_length=512, description = "recipe name")
    instructions: str = Field(..., description = "instructions for the recipe")
    time: int = Field(..., gt=0, description = 'time to make the recipe')
    owner_id: int = Field(..., gt=0, description = 'user associated with this recipe')

class recipeCreate(recipeBase): #create a recipe
    ingredients: List[recipeIngredientCreate] = Field(..., description='A list of ingredient IDs for the recipe')

class recipeModel(recipeBase): #for when you need to return everything associated with a recipe
    recipe_id: int = Field(..., description = "unique id for recipe instance")
    ingredients: List[recipeIngredientModel] = Field(default_factory=list, description= 'ingredients in the recipe')

class recipeUpdate(BaseModel): #optional parameters
    recipe_name: Optional[str] = Field(None, min_length=1, max_length=512, description = "recipe name")
    instructions: Optional[str] = Field(None, description = "instructions for the recipe")
    time: Optional[int] = Field(None, gt=0, description = 'time to make the recipe')
    owner_id: Optional[int] = Field(None, gt=0, description = 'user associated with this recipe')
    ingredients: Optional[List[recipeIngredientCreate]] = Field(None, description='A list of ingredient IDs for the recipe')


#---------------------------------------SHOPPING LIST-----------------------------------------


class shoppingBase(BaseModel): #base class
    shopping_list_name: str = Field(..., min_length=1, max_length=512, description = "shopping list name")
    owner_id: int = Field(..., gt=0, description = 'user associated with this shopping list')

class shoppingCreate(shoppingBase): #create a shopping list
    ingredients: List[shoppingIngredientCreate] = Field(..., description='A list of ingredient IDs for the shopping list')

class shoppingModel(shoppingBase): #for when you need to return everything associated with a shopping list
    shopping_list_id: int = Field(..., description = "unique id for a shopping list instance")
    ingredients: List[shoppingIngredientModel] = Field(default_factory=list, description= 'ingredients in the shopping list')


class shoppingUpdate(BaseModel): #optional parameters
    shopping_list_name: Optional[str] = Field(None, min_length=1, max_length=512, description = "shopping list name")
    owner_id: Optional[int] = Field(None, gt=0, description = 'user associated with this shopping list')
    ingredients: Optional[List[shoppingIngredientCreate]] = Field(None, description='A list of ingredient IDs for the shopping list')

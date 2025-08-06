from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
import database
import models
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/recipes', response_model=List[models.recipeModel], status_code=status.HTTP_200_OK)
def get_all_recipes(firstn: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(database.Recipe) #db.query is the money function, google it to understand the rest
    if firstn is not None and firstn > 0:
        query = query.limit(firstn) #gets only firstn results
    if firstn is not None and firstn < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The 'firstn' parameter must be a positive integer.")
    recipes = query.all()
    return recipes

@router.get("/recipes/{id}", response_model = models.recipeModel, status_code=status.HTTP_200_OK)
def get_recipe(id: int, db: Session = Depends(get_db)):
    recipe = db.query(database.Recipe).filter(database.Recipe.recipe_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe

#NEEDS UPDATING - RECIPE INGREDIENTS HANDLING
@router.post('/recipes', response_model = models.recipeModel, status_code=status.HTTP_201_CREATED)
def create_recipe(new_recipe: models.recipeCreate, db: Session = Depends(get_db)):
    new = database.Recipe(recipe_name = new_recipe.recipe_name, recipe_instructions = new_recipe.instructions, recipe_time = new_recipe.time, owner_id = new_recipe.owner_id)
    #note - this line ^ has some weird naming conventions, because I used it to clarify relationships
    db.add(new) #adds to database
    db.commit() #commits change to database
    db.refresh(new) #updates 'new' with the data from the databse

    db_recipe_ingredients = []
    for ingredient_data in new_recipe.ingredients:
        db_recipe_ingredients.append(database.RecipeIngredient(
            recipe_id=new.recipe_id, # Use the new recipe's ID
            ingredient_id=ingredient_data.ingredient_id,
            quantity=ingredient_data.quantity,
            unit=ingredient_data.unit
        ))

    #why we did it twice - had to do it the first time so that we could get a recipe id to exist lol
    db.add_all(db_recipe_ingredients)
    db.commit()
    db.refresh(new)
    return new

@router.put('/recipes/{id}', response_model = models.recipeModel, status_code=status.HTTP_200_OK)
def update_recipe(id: int, update_recipe: models.recipeUpdate, db: Session = Depends(get_db)):
    recipe = db.query(database.Recipe).filter(database.Recipe.recipe_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    update_data = update_recipe.model_dump(exclude_unset=True) 
    #model.dump - pydantic method to convery a Pydantic model to a dictionary
    #exclude_unset = True - inputted data only
    for key, value in update_data.items():
        setattr(recipe, key, value)

    db.commit()
    db.refresh(recipe)
    return recipe

@router.delete("/recipes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(id: int, db: Session = Depends(get_db)):
    recipe = db.query(database.Recipe).filter(database.Recipe.recipe_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    db.delete(recipe)
    db.commit()

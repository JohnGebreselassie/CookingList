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

@router.get('/ingredients', response_model=List[models.ingredientModel], status_code=status.HTTP_200_OK)
def get_all_ingredients(firstn: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(database.Ingredient) #db.query is the money function, google it to understand the rest
    if firstn is not None and firstn > 0:
        query = query.limit(firstn) #gets only firstn results
    if firstn is not None and firstn < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The 'firstn' parameter must be a positive integer.")
    ingredients = query.all()
    return ingredients

@router.get("/ingredients/{id}", response_model = models.ingredientModel, status_code=status.HTTP_200_OK)
def get_ingredients(id: int, db: Session = Depends(get_db)):
    ingredient = db.query(database.Ingredient).filter(database.Ingredient.ingredient_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    return ingredient


@router.post('/ingredients', response_model = models.ingredientModel, status_code=status.HTTP_201_CREATED)
def create_ingredient(new_ingredient: models.ingredientCreate, db: Session = Depends(get_db)):
    new = database.Ingredient(ingredient_name = new_ingredient.ingredient_name)
    db.add(new) #adds to database
    db.commit() #commits change to database
    db.refresh(new) #updates 'new' with the data from the databse
    return new

@router.put('/ingredients/{id}', response_model = models.ingredientModel, status_code=status.HTTP_200_OK)
def update_ingredient(id: int, update_ingredient: models.ingredientUpdate, db: Session = Depends(get_db)):
    ingredient = db.query(database.Ingredient).filter(database.Ingredient.ingredient_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    
    update_data = update_ingredient.model_dump(exclude_unset=True) 
    #model.dump - pydantic method to convery a Pydantic model to a dictionary
    #exclude_unset = True - inputted data only
    for key, value in update_data.items():
        setattr(ingredient, key, value)

    db.commit()
    db.refresh(ingredient)
    return ingredient

@router.delete("/ingredients/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(id: int, db: Session = Depends(get_db)):
    ingredient = db.query(database.Ingredient).filter(database.Ingredient.ingredient_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    
    db.delete(ingredient)
    db.commit()

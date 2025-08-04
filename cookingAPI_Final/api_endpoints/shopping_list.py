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

@router.get('/shopping_lists', response_model=List[models.shoppingModel], status_code=status.HTTP_200_OK)
def get_all_shopping_lists(firstn: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(database.ShoppingList) #db.query is the money function, google it to understand the rest
    if firstn is not None and firstn > 0:
        query = query.limit(firstn) #gets only firstn results
    if firstn is not None and firstn < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The 'firstn' parameter must be a positive integer.")
    shopping_list = query.all()
    return shopping_list

@router.get("/shopping_lists/{id}", response_model = models.shoppingModel, status_code=status.HTTP_200_OK)
def get_shopping_list(id: int, db: Session = Depends(get_db)):
    shopping_list = db.query(database.ShoppingList).filter(database.ShoppingList.shopping_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not shopping_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping list not found")
    return shopping_list

#THIS MODEL NEEDS UPDATING TOMORROW - INGREDIENTS NEEDS TO BE ADDED TO OTHER TABLE
@router.post('/shopping_lists', response_model = models.shoppingModel, status_code=status.HTTP_201_CREATED)
def create_shopping_list(new_shopping_list: models.shoppingCreate, db: Session = Depends(get_db)):
    new = database.ShoppingList(shopping_name = new_shopping_list.shopping_list_name, owner_id = new_shopping_list.owner_id)
    db.add(new) #adds to database
    db.commit() #commits change to database
    db.refresh(new) #updates 'new' with the data from the databse
    return new

@router.put('/shopping_lists/{id}', response_model = models.shoppingModel, status_code=status.HTTP_200_OK)
def update_shopping_list(id: int, update_shopping_list: models.shoppingUpdate, db: Session = Depends(get_db)):
    shopping_list = db.query(database.ShoppingList).filter(database.ShoppingList.shopping_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not shopping_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping List not found")
    
    update_data = update_shopping_list.model_dump(exclude_unset=True) 
    #model.dump - pydantic method to convery a Pydantic model to a dictionary
    #exclude_unset = True - inputted data only
    for key, value in update_data.items():
        setattr(shopping_list, key, value)

    db.commit()
    db.refresh(shopping_list)
    return shopping_list

@router.delete("/shopping_lists/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shopping_list(id: int, db: Session = Depends(get_db)):
    shopping_list = db.query(database.ShoppingList).filter(database.ShoppingList.shopping_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not shopping_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping list not found")
    
    db.delete(shopping_list)
    db.commit()

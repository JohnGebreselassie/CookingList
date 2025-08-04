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

@router.get('/users', response_model=List[models.userModel], status_code=status.HTTP_200_OK)
def get_all_users(firstn: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(database.User) #db.query is the money function, google it to understand the rest
    if firstn is not None and firstn > 0:
        query = query.limit(firstn) #gets only firstn results
    if firstn is not None and firstn < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The 'firstn' parameter must be a positive integer.")
    users = query.all()
    return users

@router.get("/users/{id}", response_model = models.userModel, status_code=status.HTTP_200_OK)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(database.User).filter(database.User.user_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post('/users', response_model = models.userModel, status_code=status.HTTP_201_CREATED)
def create_user(new_user: models.userCreate, db: Session = Depends(get_db)):
    new = database.User(username = new_user.username, password = new_user.password)
    db.add(new) #adds to database
    db.commit() #commits change to database
    db.refresh(new) #updates 'new' with the data from the databse
    return new

@router.put('/users/{id}', response_model = models.userModel, status_code=status.HTTP_200_OK)
def update_user(id: int, update_user: models.userUpdate, db: Session = Depends(get_db)):
    user = db.query(database.User).filter(database.User.user_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = update_user.model_dump(exclude_unset=True) 
    #model.dump - pydantic method to convery a Pydantic model to a dictionary
    #exclude_unset = True - inputted data only
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_users(id: int, db: Session = Depends(get_db)):
    user = db.query(database.User).filter(database.User.user_id == id).first() #queries the database, .filter adds a WHERE sql function
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()

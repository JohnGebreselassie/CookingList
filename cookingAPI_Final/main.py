from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import database
import models
from sqlalchemy.orm import Session

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/get{id}", response_model = models.userModel)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(database.User).filter(database.User.user_id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post('/users/create', response_model = models.userModel)
def create_user(new_user: models.userCreate, db: Session = Depends(get_db)):
    new = database.User(username = new_user.username, password = new_user.password)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new
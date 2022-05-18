
from statistics import mode
from fastapi import FastAPI, Depends, Query, status, HTTPException
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models

from pydantic import BaseModel

class Test(BaseModel):
    first_name:str
    last_name:str
    email:str
    password_hash:str


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LabFull API", version="0.0.1")


@app.get("/api/user", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    """Returns all users in the database."""

    all_users = db.query(models.User).all()
    return {"data":all_users}



@app.get("/api/user/{id}",status_code=status.HTTP_200_OK)
async def get_single_user(id: int, db: Session = Depends(get_db)):
    """Returns a single user based on id."""

    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"data":user}



@app.post("/api/user", status_code=status.HTTP_201_CREATED)
async def create_new_user(user:Test, db: Session = Depends(get_db)):
    """Creates a new user in the database."""
    
    new_user= models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {new_user}




@app.delete("/api/user/{id}")
async def delete_user(id:int, db: Session = Depends(get_db)):
    """Deletes a user in the database based on id."""

    user = db.query(models.User).filter(models.User.id == id).first()


    if user == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    db.delete(user)
    db.commit()

    return None




# @app.put("/api/user/{id}")
# async def update_user(id:int,updated_user:Test, db: Session = Depends(get_db) ):
#     """Updates all the attribue columns for a user based on id."""

#     query = db.query(models.User).filter(models.User.id == id)

#     user = query.first()

#     if user == None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

#     updated_u = query.update(updated_user.dict())

#     db.commit()
#     db.refresh(updated_u)
    

#     return {user}



@app.get("/")
async def root():
    return {"message":"Hello Worldd"}
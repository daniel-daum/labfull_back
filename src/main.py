from fastapi import FastAPI, Depends
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

app = FastAPI()


@app.get("/user")
def get_users(db: Session = Depends(get_db)):

    all_users = db.query(models.User).all()
    return {"data":all_users}

@app.get("/user/{id}")
def get_single_user(id: int, db: Session = Depends(get_db)):


    # user = db.query(models.P)
    return {"msg":"unfinished"}


@app.post("/dogs")
def create_posts(user:Test, db: Session = Depends(get_db)):
    

    
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {new_user}

@app.get("/")
async def root():
    return {"message":"Hello Worldd"}
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from .. database import get_db
from fastapi import Depends, status, HTTPException, APIRouter

router = APIRouter(tags=["Users"], prefix="/api/users")

# GET ALL USERS
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User], tags=["Users"])
async def get_users(db: Session = Depends(get_db)):
    """Returns all users in the database."""

    all_users = db.query(models.User).all()

    if all_users == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no users in the database.")

    return all_users


# GET ONE USER BY ID
@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.User, tags=["Users"])
async def get_single_user(id: int, db: Session = Depends(get_db)):
    """Returns a single user based on id."""

    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")

    return user


# CREATE A NEW USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User, tags=["Users"])
async def create_new_user(user:schemas.CreateUser, db: Session = Depends(get_db)):
    """Creates a new user in the database."""

    hashed_password = utils.hash(user.password)

    user.password = hashed_password
 
    new_user= models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
 

    return new_user



# DELETE A USER BY ID
@router.delete("/{id}", tags=["Users"])
async def delete_user(id:int, db: Session = Depends(get_db)):
    """Deletes a user in the database based on id."""

    user = db.query(models.User).filter(models.User.id == id).first()


    if user == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")

    db.delete(user)
    db.commit()

    return None



# UPDATE A USER BY ID
@router.put("/api/users/{id}",status_code=status.HTTP_200_OK, response_model=schemas.User, tags=["Users"])
async def update_user(id:int, new_data:schemas.UpdateUser, db: Session = Depends(get_db)):
    """Updates all the attribue columns for a user based on id."""

    get_user_query = db.query(models.User).filter(models.User.id == id)

    old_user_data =  get_user_query.first()
    
    if old_user_data == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")

    get_user_query.update(new_data.dict(),synchronize_session=False)

    db.commit()

    return get_user_query.first()
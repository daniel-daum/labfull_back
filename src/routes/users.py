from sqlalchemy.orm import Session
from typing import List

from ..utilities import crud
from ..utilities import oauth2
from ..database import schemas
from ..database.database import get_db
from fastapi import Depends, status, HTTPException, APIRouter


router = APIRouter(tags=["Users"], prefix="/api/users")

# GET ALL USERS


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User], tags=["Users"])
async def get_users(db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    """Returns all users in the database."""

    users = crud.get_all_users(db)

    if users == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no users in the database.")

    return users


# GET ONE USER BY ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User, tags=["Users"])
async def get_single_user_id(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    """Returns a single user based on id."""

    user = crud.get_user_by_id(db, id)

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")

    return user


# CREATE A NEW USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User, tags=["Users"])
async def create_new_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    """Creates a new user in the database."""

    db_user = crud.get_user_by_email(db, user)

    if db_user == None:
        new_user = crud.create_user(db, user)
    else:
        raise HTTPException(status_code=400, detail="Email already registered")

    return new_user


# DELETE A USER BY ID
@router.delete("/{id}", tags=["Users"])
async def delete_user(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    """Deletes a user in the database based on id."""

    user = crud.get_user_by_id(db, id)

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")

    crud.delete_user(db, user)

    return None



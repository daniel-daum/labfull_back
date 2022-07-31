from sqlalchemy.orm import Session
from typing import List

from ..utilities import crud, oauth2, utils
from ..database import schemas
from ..database.database import get_db
from fastapi import Depends, status, HTTPException, APIRouter
from src.settings import settings


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

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")

    return user


# CREATE A NEW USER
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User, tags=["Users"])
async def create_new_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    """Creates a new user in the database."""

    db_user = crud.get_user_by_email(db, user)

    email_validation_flag = utils.check_email(user)

# Checks if user email has @wustl.edu extension
    if email_validation_flag:

        # checks if user already exists in the database.
        if db_user is None:

            # CREATES A NEW USER IN THE DB
            new_user = crud.create_user(db, user)

            # CREATES A JWT FOR EMAIL VERIFICATION
            token = oauth2.create_access_token(
                data={"user_id": new_user.id, "users_email": new_user.email})

            # SENDS AN EMAIL WITH THE JWT
            crud.send_verification_email(db, token, new_user)

        else:
            raise HTTPException(
                status_code=400, detail="Email already registered")
    else:
        raise HTTPException(
            status_code=400, detail="You must register with a @wustl.edu email address.")

    return new_user


# DELETE A USER BY ID
@router.delete("/{id}", tags=["Users"])
async def delete_user(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    """Deletes a user in the database based on id."""

    user = crud.get_user_by_id(db, id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")

    crud.delete_user(db, user)

    return None

# # UPDATE A USERS FIRST NAME
# @router.patch("/first_name", tags=['Users'], response_model=schemas.UpdateFirstName)
# async def update_user_first_name(new_first_name:schemas.UpdateFirstName, db: Session = Depends(get_db), current_user_id:int = Depends(oauth2.get_current_user)):
#     """Updates the current users first name."""
#     user = crud.update_user_first_name(db, current_user_id, new_first_name)

#     return  user

# # UPDATES A USERS LAST NAME
# @router.patch("/last_name", tags=["Users"], response_model=schemas.UpdateLastName)
# async def update_user_last_name(new_last_name:schemas.UpdateLastName, db: Session = Depends(get_db), current_user_id:int = Depends(oauth2.get_current_user)):
#     """Updates the current users last name."""

#     user = crud.update_user_last_name(db, current_user_id, new_last_name)

#     return user

# # UPDATES A USERS EMAIL
# @router.patch("/email", tags=["Users"], response_model=schemas.UpdateEmail)
# async def update_user_email(new_email:schemas.UpdateEmail,db: Session = Depends(get_db), current_user_id:int = Depends(oauth2.get_current_user)):
#     """Updates the current users email."""

#     user = crud.update_user_email(db, current_user_id, new_email)

#     return user

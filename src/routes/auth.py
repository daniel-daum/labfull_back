from msilib import schema
from fastapi import Depends, status, HTTPException, APIRouter

from ..utilities import oauth2

from ..database import models

from src.database import schemas
from ..utilities import utils, crud
from ..database.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.settings import settings


router = APIRouter(tags=["Authentication"], prefix="/api/auth")


@router.post("/login", tags=["Authentication"], response_model=schemas.Token)
async def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticates user credentials and generates a JWT"""
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # CREATE AN ACCESS TOKEN
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    blacklist_token = {"token":access_token, "users_id":user.id}

    # Add TOKEN TO BLACKLIST TABLE
    crud.add_token_to_blist(db, blacklist_token)

    # UPDATE USERS LAST LOGIN
    crud.update_last_login(db,user.id)

    return {"access_token":access_token, "token_type":"bearer"}


@router.get("/verify_email/{token}", tags=["Authentication"], response_model=schemas.User)
async def verify_email(token:str, db: Session = Depends(get_db)):

    # Create a credentials exception
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate email credentials", headers={"WWW-Authenticate":"Bearer"})

    # Recieve, deconstruct, verify token is valid
    payload = oauth2.verify_access_token(token, credentials_exception)

    # Update email verified column to True
    db.query(models.User).filter(models.User.id == payload.id).update({models.User.email_verified:True}, synchronize_session=False)
    db.commit()

    user = crud.get_user_by_id(db, payload.id)

    #Give user permissions in permissions table after email is verfied
    role_data = {"users_id":payload.id,"role":f"{settings.ROLE}", "admin_created_by":f"{settings.ADMIN}"}

    crud.create_role(db, role_data)

    return user
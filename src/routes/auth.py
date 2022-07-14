from fastapi import Depends, status, HTTPException, APIRouter

from ..utilities import oauth2

from ..database import models

from ..database import schemas
from ..utilities import utils, crud
from ..database.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"], prefix="/api/auth")


@router.post("/login", tags=["Authentication"], response_model=schemas.Token)
async def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticates user credentials and generates a JWT"""
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    #Creation of access token
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    blacklist_token = {"token":access_token, "users_id":user.id}

    #Add JWT TO BLACKLIST TABLE
    crud.add_token_to_blist(db, blacklist_token)

    return {"access_token":access_token, "token_type":"bearer"}


# @router.post("/verify_access", tage=["Authentication"], response_model=schemas.authorized_response)
# async def verify(request: schemas.check_if_authorized,db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
#     """Verifies if a user has permissions to access a specific page on the website."""



    



#     return
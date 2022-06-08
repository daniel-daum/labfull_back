from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import session

from ..schemas import schemas

from ..models import database
from ..models import models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
load_dotenv("./.env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = os.getenv("SECRETKEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKENEXPIRE"))

def create_access_token(data:dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_key = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

    return encoded_key


def verify_access_token(token:str, credentials_exception):

    try:

        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
            
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data




def get_current_user(token: str = Depends(oauth2_scheme), db:session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token, credentials_exception)

    current_user = db.query(models.User).filter(models.User.id == token.id).first()

    return current_user





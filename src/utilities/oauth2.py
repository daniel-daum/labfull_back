from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import session
from ..database import schemas
from ..database import database
from ..database import models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

KEY = settings.KEY
ALGO = settings.ALGO
EXPIRE_MINUTES = int(settings.EXPIRE)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_key = jwt.encode(to_encode, KEY, algorithm=ALGO)

    return encoded_key


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, KEY, algorithms=[ALGO])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    current_user = db.query(models.User).filter(
        models.User.id == token.id).first()

    return current_user.id

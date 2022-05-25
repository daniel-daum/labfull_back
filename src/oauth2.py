from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv("./.env")


SECRET_KEY = os.getenv("SECRETKEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("TOKENEXPIRE")

def create_access_token(data:dict):

    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_key = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

    return encoded_key


# def verify_access_token(token:str, credentials_exception):

#     payload = jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)
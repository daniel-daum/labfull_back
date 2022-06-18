from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):

    return pwd_context.verify(plain_password,hashed_password)

# def check_email(user: schemas.CreateUser):
#     """Checks if user email has @wustl.edu extension"""

#     suffix ="wustl.edu"

#     email = user.email.strip()
#     split_email = email.split("@")
#     email_suffix = split_email[1]

#     if email_suffix == suffix:
#         return True

#     return False
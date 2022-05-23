from pydantic import BaseModel, EmailStr
from pydantic.schema import Optional
from datetime import datetime

# Base User Schema
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

# Create New User Schema
class CreateUser(UserBase):
    password: str

    class Config:
          orm_mode = True

# Update Existing User - ALL ATTRIBUTES Schema
class UpdateUser(CreateUser):
    pass

    class Config:
          orm_mode = True



# User Response Schema
class User(UserBase):
      id: int
      created_at: datetime

      class Config:
          orm_mode = True



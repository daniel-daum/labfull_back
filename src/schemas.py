from pydantic import BaseModel
from datetime import datetime

# Base User Schema
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

# Create New User Schema
class CreateUser(UserBase):
    password_hash: str

    class Config:
          orm_mode = True

# Update Existing User - ALL ATTRIBUTES Schema
class UpdateUser(CreateUser):
    pass

# User Response Schema
class User(UserBase):
      created_at: datetime

      class Config:
          orm_mode = True



from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date

#-----------------users-schemas------------------------------------


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

#------------------supplies-schemas------------------------------------

class SuppliesBase(BaseModel):
    item_name:str
    quantity:int
    class Config:
          orm_mode = True


class CreateSupply(SuppliesBase):
    date_ordered: date
    temp_sensitive: str
    order_status:Optional[str]
    owner_id:str

    class Config:
          orm_mode = True


class UpdateSupply(CreateSupply):
    pass

    class Config:
          orm_mode = True

class Supply(SuppliesBase):
    id: int
    date_ordered: date
    temp_sensitive: str
    owner_id:str
    recieved_by:Optional[str]
    owner_id:str
    created_at:datetime
    order_status:Optional[str]


    class Config:
          orm_mode = True
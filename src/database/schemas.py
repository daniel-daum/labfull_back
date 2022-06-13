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


# User Response Schema
class User(UserBase):
      id: int
      created_at: datetime

      class Config:
          orm_mode = True

#Update User First Name
class UpdateFirstName(BaseModel):
    first_name:str
    class Config:
          orm_mode = True

class UpdateLastName(BaseModel):
    last_name:str
    class Config:
          orm_mode = True

class UpdateEmail(BaseModel):
    email:EmailStr
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
    users_id:int

    class Config:
          orm_mode = True


class UpdateSupply(CreateSupply):
    order_status:Optional[str]

    class Config:
          orm_mode = True

class Supply(SuppliesBase):
    id: int
    date_ordered: date
    temp_sensitive: str
    recieved_by:Optional[str]
    users_id:int
    created_at:datetime
    order_status:Optional[str]


    class Config:
          orm_mode = True

class UpdateOrderedStatus(BaseModel):
    order_status:str
        
    class Config:
         orm_mode = True


#------------------Authentication------------------------------------

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None




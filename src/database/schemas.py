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
    email_verified:Optional[bool]

    class Config:
          orm_mode = True


# User Response Schema
class User(UserBase):
      id: int
      created_at: datetime
      email_verified:Optional[bool]

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
    temp_sensitive: bool
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
    temp_sensitive: bool
    recieved_by:Optional[str]
    users_id:int
    created_at:datetime
    order_status:Optional[str]
    last_modified_at:Optional[datetime]


    class Config:
          orm_mode = True

# Update Order status
class UpdateSupply(BaseModel):
    id: int
    item_name:Optional[str]
    temp_sensitive:Optional[bool]
    recieved_by:Optional[int]
    quantity:Optional[str]
        
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
    users_email:Optional[str] = None
    

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Check if authorized schemas

class check_if_authorized(Token):
    page_name:str

class authorized_response(BaseModel):
    """Response model if authorized to access a page."""
    authorized: bool

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create Role  Schema and Response
class CreateRole(BaseModel):
    """Create a Role Schema"""
    users_id:int
    role:str
    admin_created_by:str

class GetRoleResponse(CreateRole):
    """Create a Role response Schema"""
    created_at: datetime


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# JWT Token blacklist schemas

class addToken(BaseModel):
    token:str
    users_id=int

class getBlackJWT(addToken):
    created_at: datetime
    id:int
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Email verification schemas
class EmailVerify(BaseModel):
    id:int
    temp_jwt:str
    users_id:int
    users_email:str

class EmailVerifyResponse(EmailVerify):
    created_at:datetime

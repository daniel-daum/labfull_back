
from email.policy import default
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Date, null, Boolean
from sqlalchemy.sql.expression import text
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)    
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_login = Column(TIMESTAMP(timezone=True))
    email_verified = Column(Boolean, default=False)

class Email_Verification(Base):
    __tablename__ = "email_verification"

    id = Column(Integer, primary_key=True, nullable=False)
    temp_jwt = Column(String(255), nullable=False)
    users_id = Column(Integer, nullable=False)
    users_email = Column(String(100), ForeignKey("users.email"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User_Roles(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, nullable=False)
    users_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(255), nullable=False)
    admin_created_by = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Site_permissions(Base):
    __tablename__ = "site_permissions"

    id = Column(Integer, primary_key=True, nullable=False)
    page_name = Column(String(255), nullable=False)
    role_required = Column(String(255), nullable=False)
    admin_created_by = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Token_list(Base):
    __tablename__ = "token_list"

    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(String(255), nullable=False)
    users_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    date_ordered = Column(Date, nullable=False)
    order_status = Column(String(20), default="ordered")
    recieved_by = Column(String(255))
    temp_sensitive = Column(Boolean)
    users_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_modified_at = Column(TIMESTAMP(timezone=True))

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)    
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column()

    supplies = relationship("Supply", back_populates="owner")


class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    date_ordered = Column()
    order_status = Column(String(20), nullable=False)
    temp_sensitive = Column(String(20), nullable=False)
    recieved_by = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="supplies")

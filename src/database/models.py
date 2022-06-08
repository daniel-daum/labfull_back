
from sqlalchemy import TIMESTAMP, Column, DateTime, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
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

    # supplies = relationship("Supply", back_populates="owner")


class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    date_ordered = Column(Date, nullable=False)
    order_status = Column(String(20), default="ordered")
    temp_sensitive = Column(String(20))
    recieved_by = Column(String(255))
    users_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # owner = relationship("User", back_populates="supplies")

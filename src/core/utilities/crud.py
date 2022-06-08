from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas
from . import utils

# GET ALL USERS
def get_all_users(db: Session):
    """Returns all users in the database."""

    return db.query(models.User).all()

# GET ONE USER BY ID
def get_user_by_id(db: Session, id: int):
    """Returns a single user based on id."""

    return db.query(models.User).filter(models.User.id == id).first()

# GET ONE USER BY EMAIL
def get_user_by_email(db: Session, user: schemas.CreateUser):
    """Returns a single user based on email."""

    return db.query(models.User).filter(models.User.email == user.email).first()

# CREATE NEW USER
def create_user(db: Session, user: schemas.CreateUser):
    """Creates a new user in the database."""

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# DELETE A USER
def delete_user(db: Session, user: schemas.User):
    """Deletes a user in the database based on id."""

    db.delete(user)
    db.commit()

    return None

# UPDATE A USER - ALL
def update_user(db: Session, id: int, user: schemas.User):
    """Updates all the attribue columns for a user based on id."""

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user = db.query(models.User).filter(models.User.id == id).update(
        user.dict(), synchronize_session=False)

    db.commit()

    return get_user_by_id(db,id)

# GET ALL SUPPLIES
def get_all_supplies(db:Session):
    """Returns all supplies in the database."""

    return db.query(models.Supply).all()

# GET ONE SUPPLY BY ID
def get_supply_by_id(db:Session, id:int):
    """Gets a single supply item from the database based on id."""

    return db.query(models.Supply).filter(models.Supply.id == id).first()

# CREATE A NEW SUPPLY ITEM
def create_new_supply(db:Session, supply:schemas.CreateSupply):
    """Creates a new supply item in the database."""

    new_supply_item = models.Supply(**supply.dict())

    db.add(new_supply_item)
    db.commit()
    db.refresh(new_supply_item)

    return new_supply_item

# DELETE A SUPPLY ITEM
def delete_supply_item(db:Session, supply:schemas.Supply):
    """Deletes a supply item from the database based on id."""

    db.delete(supply)
    db.commit()

    return None

# UPDATE A SUPPLY ITEM - ALL ATTRIBUTES
def update_supply_item(db:Session, id:int, supply:schemas.Supply):

    db.query(models.Supply).filter(models.Supply.id == supply.id).update(supply.dict(), synchrnoize_session=False)

    db.commit()

    return get_supply_by_id(db, id)
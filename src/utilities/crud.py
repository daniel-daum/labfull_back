from sqlalchemy.orm import Session

from src.utilities import oauth2
from ..database import models
from ..database import schemas
from . import utils
from datetime import datetime
from src.settings import settings
import smtplib
import ssl
from email.message import EmailMessage

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# GET ALL USERS
def get_all_users(db: Session):
    """Returns all users in the database."""

    return db.query(models.User).all()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# GET ONE USER BY ID
def get_user_by_id(db: Session, id: int):
    """Returns a single user based on id."""

    return db.query(models.User).filter(models.User.id == id).first()
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


# GET ONE USER BY EMAIL
def get_user_by_email(db: Session, user: schemas.CreateUser):
    """Returns a single user based on email."""

    return db.query(models.User).filter(models.User.email == user.email).first()
 # ------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# DELETE A USER
def delete_user(db: Session, user: schemas.User):
    """Deletes a user in the database based on id."""

    db.delete(user)
    db.commit()

    return None

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# UPDATE A USER - ALL
def update_user(db: Session, id: int, user: schemas.User):
    """Updates all the attribue columns for a user based on id."""

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user = db.query(models.User).filter(models.User.id == id).update(
        user.dict(exclude_unset=True), synchronize_session=False)

    db.commit()

    return get_user_by_id(db,id)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# UPDATES A USERS FIRST NAME
def update_user_first_name(db: Session, current_user_id:int, new_name:schemas.UpdateFirstName):
    """Updates a users first name"""

    db.query(models.User).filter(models.User.id == current_user_id).update({models.User.first_name:new_name.first_name})

    db.commit()

    return get_user_by_id(db, current_user_id)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# UPDATES A USERS LAST NAME
def update_user_last_name(db: Session, current_user_id:int, new_name:schemas.UpdateLastName):
    """Updates a users first name"""

    db.query(models.User).filter(models.User.id == current_user_id).update({models.User.last_name:new_name.last_name})

    db.commit()

    return get_user_by_id(db, current_user_id)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


# UPDATES A USERS EMAIL
def update_user_email(db: Session, current_user_id:int, new_email:schemas.UpdateEmail):
    """Updates a users email"""

    db.query(models.User).filter(models.User.id == current_user_id).update({models.User.email:new_email.email})

    db.commit()

    return get_supply_by_id(db, current_user_id)


# -----------------------------------------------------------------------------------------------------------------------------------------------------------

# CREATE NEW USER ROLE
def create_role(db: Session, role:schemas.CreateRole):
    """Adds a 'role' to a user in the roles table. i.e. User or Admin"""

    new_role = models.User_Roles(**role)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)


    return new_role

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Add JWT Token to blacklist table after creation
def add_token_to_blist(db: Session, token:schemas.addToken):

    issued_token = models.Token_list(**token)

    db.add(issued_token)
    db.commit()
    db.refresh(issued_token)

    return issued_token

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Updates last login date.


def update_last_login(db:Session, user_id:int):

    current_datetime = datetime.now()

    db.query(models.User).filter(models.User.id == user_id).update({models.User.last_login:current_datetime})

    db.commit()


    return get_user_by_id(db, user_id)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Updates a supply order status

def update_supply_order_status(db:Session, status:schemas.UpdateSupply):

    db.query(models.Supply).filter(models.Supply.id == status.id).update({models.Supply.order_status:status.order_status})

    db.commit()

    return get_supply_by_id(db, status.id)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Updates a supply recieved by

def update_supply_item_recieved_by(db:Session, status:schemas.UpdateSupply):

    db.query(models.Supply).filter(models.Supply.id == status.id).update({models.Supply.recieved_by:status.recieved_by})

    db.commit()

    return get_supply_by_id(db, status.id)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Updates a supply item name

def update_supply_item_name(db:Session,status:schemas.UpdateSupply):

    db.query(models.Supply).filter(models.Supply.id == status.id).update({models.Supply.item_name:status.item_name})

    db.commit()

    return get_supply_by_id(db, status.id)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Updates a supply item name

def update_supply_item_quantity(db:Session,status:schemas.UpdateSupply):

    db.query(models.Supply).filter(models.Supply.id == status.id).update({models.Supply.quantity:status.quantity})

    db.commit()

    return get_supply_by_id(db, status.id)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Updates a supply temp sensitive

def update_supply_item_temp_sensitive(db:Session,status:schemas.UpdateSupply):

    db.query(models.Supply).filter(models.Supply.id == status.id).update({models.Supply.temp_sensitive:status.temp_sensitive})

    db.commit()

    return get_supply_by_id(db, status.id)



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Updates last supply item modified time


def update_supply_last_modified(db:Session, supply_id:int):

    current_datetime = datetime.now()

    db.query(models.Supply).filter(models.Supply.id == supply_id).update({models.Supply.last_modified_at:current_datetime})

    db.commit()


    return get_supply_by_id(db, supply_id)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# # VERIFY USER PERMISSIONS

# def get_permissiosn(db:Session, user_id:int):

#   return db.query(models.User_Roles).filter(models.User_Roles.users_id == user_id).first()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# SENDS A VERIFICATION EMAIL WITH A LINK. LINK IS TO VERIFY EMAIL POST ROUTE AND INCLUDES A JWT 
def send_verification_email(db:Session, token:str, user:schemas.User):

    # Pack user data and token string into a dict
    user_dict = {"users_id":user.id, "users_email":user.email, "temp_jwt":token}

    # Add dict data into table model
    temp_user_verification_info = models.Email_Verification(**user_dict)


    #AAdd user data to the database
    db.add(temp_user_verification_info)
    db.commit()

    # Generate and send an email to the user with verification information.
    msg = EmailMessage()

    msg['Subject'] = "LabFull - Verify Your Email Address"
    msg['From'] = settings.EMAIL
    msg['To'] = "daniel_daum@outlook.com"
    msg.set_content(f'''
    <html lang="en">
    <body style="font-family:Arial, Helvetica, sans-serif ;">

    <p>Hello, {user.first_name.title()}!</p>

    <p> Please click the button below to verify your email address and complete registration for LabFull</p>  

    <div>
        <p style="font-weight: 700; color:black; font-size:1em; padding: .3em;"><a href="http://localhost:8000/api/auth/verify_email/{token}" style="text-decoration: underline; color:black" >Verify Your Email Address</a></p>
    </div>


    <p>This email was sent to: {user.email.upper()}

        Please do not reply to this message.
        
        LabFull will never contact you by email asking you to validate your personal information such as your password. If you recieve such a request please contact us at <span style="text-decoration: underline ;">labfull@proton.me</span></p>
    
    </body>
    </html>
    ''', subtype='html')

    context = ssl.create_default_context()

 

    with smtplib.SMTP_SSL(settings.EMAIL_SERVER, 465, context=context) as smtp:
        smtp.login(settings.EMAIL, settings.EMAIL_SERVER_KEY)
        smtp.send_message(msg)
        smtp.quit()

    return


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

async def get_verification_jwt(db:Session, id:int):

    verify_db_user = db.query(models.Email_Verification).filter(models.Email_Verification.id == id).first()

    return verify_db_user
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# GET ALL SUPPLIES
def get_all_supplies(db:Session):
    """Returns all supplies in the database."""
    return db.query(models.Supply).all()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# GET ONE SUPPLY BY ID
def get_supply_by_id(db:Session, id:int):
    """Gets a single supply item from the database based on id."""

    return db.query(models.Supply).filter(models.Supply.id == id).first()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CREATE A NEW SUPPLY ITEM
def create_new_supply(db:Session, supply:schemas.CreateSupply):
    """Creates a new supply item in the database."""

    new_supply_item = models.Supply(**supply.dict())

    db.add(new_supply_item)
    db.commit()
    db.refresh(new_supply_item)

    return new_supply_item

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# DELETE A SUPPLY ITEM
def delete_supply_item(db:Session, supply:schemas.Supply):
    """Deletes a supply item from the database based on id."""

    db.delete(supply)
    db.commit()

    return None

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from ..core.utilities import oauth2

from ..core.models import models

from ..core.schemas import schemas
from ..core.utilities import crud
from sqlalchemy.orm import Session
from ..core.models.database import get_db

router = APIRouter(tags=["Supplies"],prefix="/api/supplies")

# GET ALL SUPPLIES
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Supply], tags=["Supplies"])
async def get_supplies(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """Returns all supplies in the database."""

    # all_supplies = db.query(models.Supply).all()

    supplies = crud.get_all_supplies(db)

    if supplies == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no users in the database.")

    return supplies


# GET A SUPPLY ITEM BY ID
@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.Supply, tags=["Supplies"] )
async def get_single_supply(id:int,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """Gets a single supply item from the database based on id."""

    # supply = db.query(models.Supply).filter(models.Supply.id == id).first()

    supply = crud.get_supply_by_id(db,id)

    if supply == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supply Item with the id:{id} was not found.")

    return supply


# CREATE A NEW SUPPLY ITEM
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Supply, tags=["Supplies"])
async def create_new_supply(supply:schemas.CreateSupply, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """Creates a new supply item in the database."""

    # new_supply_item = models.Supply(**supply.dict())

    # db.add(new_supply_item)
    # db.commit()
    # db.refresh(new_supply_item)

    # return new_supply_item
    return crud.create_new_supply(db, supply)

# DELETE A SUPPLY ITEM
@router.delete("/{id}", tags=["Supplies"])
async def delete_supply_item(id:int,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """Deletes a supply item from the database based on id."""

    supply = crud.get_supply_by_id(db, id)

    if supply == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supply with id: {id} was not found.")

    crud.delete_supply_item(db,supply)

    return None
    
    
    # supply_item = db.query(models.Supply).filter(models.Supply.id == id).first()

    # if supply_item == None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")

    # if current_user != supply_item.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    # db.delete(supply_item)
    # db.commit()

    # return None

# UPDATE A SUPPLY ITEM - ALL ATTRIBUTES
@router.put("/{id}", tags=["Supplies"], response_model=schemas.Supply)
async def update_supply_item(id:int, new_supply_data:schemas.UpdateSupply,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """Updates all attribute columns for a upply item in the database."""

    supply = crud.get_supply_by_id(db, id)

    if supply == None:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")

    updated_supply_item = crud.update_supply_item(db, id, new_supply_data)

    return updated_supply_item

    # query_item = db.query(models.Supply).filter(models.Supply.id == id) 

    # old_supply_data = query_item.first()

    # if old_supply_data== None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")

    # query_item.update(new_supply_data.dict(), synchronize_session=False)

    # db.commit()

    # return query_item.first()
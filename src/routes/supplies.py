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

    supplies = crud.get_all_supplies(db)

    if supplies == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no users in the database.")

    return supplies


# GET A SUPPLY ITEM BY ID
@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.Supply, tags=["Supplies"] )
async def get_single_supply(id:int,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """Gets a single supply item from the database based on id."""

    supply = crud.get_supply_by_id(db,id)

    if supply == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supply Item with the id:{id} was not found.")

    return supply


# CREATE A NEW SUPPLY ITEM
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Supply, tags=["Supplies"])
async def create_new_supply(supply:schemas.CreateSupply, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """Creates a new supply item in the database."""

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


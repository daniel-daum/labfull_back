from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from ..utilities import crud
from ..utilities import oauth2
from ..database import schemas
from sqlalchemy.orm import Session
from ..database.database import get_db

router = APIRouter(tags=["Supplies"], prefix="/api/supplies")

# GET ALL SUPPLIES


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Supply], tags=["Supplies"])
async def get_supplies(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Returns all supplies in the database."""

    supplies = crud.get_all_supplies(db)

    if supplies == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no supplies in the database.")

    return supplies


# GET A SUPPLY ITEM BY ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Supply, tags=["Supplies"])
async def get_single_supply(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Gets a single supply item from the database based on id."""

    supply = crud.get_supply_by_id(db, id)

    if supply == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Supply Item with the id:{id} was not found.")

    return supply


# CREATE A NEW SUPPLY ITEM
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Supply, tags=["Supplies"])
async def create_new_supply(supply: schemas.CreateSupply, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Creates a new supply item in the database."""

    return crud.create_new_supply(db, supply)

# DELETE A SUPPLY ITEM


@router.delete("/{id}", tags=["Supplies"])
async def delete_supply_item(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Deletes a supply item from the database based on id."""

    supply = crud.get_supply_by_id(db, id)

    if supply == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Supply with id: {id} was not found.")

    crud.delete_supply_item(db, supply)

    return None


# UPDATE SUPPLY ORDER STATUS
@router.patch("/order_status/", tags=['Supplies'], response_model=schemas.Supply, status_code=status.HTTP_200_OK)
async def update_order_status(supply: schemas.UpdateSupply, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    supply_db = crud.get_supply_by_id(db, supply.id)

    if supply_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Supply with id: {supply.id} was not found.")

    # Update the supply order status
    updated_supply = crud.update_supply_order_status(db, supply)

    # updated the last modified column
    crud.update_supply_last_modified(db, supply.id)

    return updated_supply

# UPDATE SUPPLY ITEM NAME


@router.patch("/item_name/", tags=['Supplies'], response_model=schemas.Supply, status_code=status.HTTP_200_OK)
async def update_supply_name(supply: schemas.UpdateSupply, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    supply_db = crud.get_supply_by_id(db, supply.id)

    if supply_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Supply with id: {supply.id} was not found.")

    updated_supply = crud.update_supply_item_name(db, supply)

    crud.update_supply_last_modified(db, supply.id)

    return updated_supply


# UPDATE SUPPLY ITEM QUANTITY
@router.patch("/quantity/", tags=['Supplies'], response_model=schemas.Supply, status_code=status.HTTP_200_OK)
async def update_supply_name(supply: schemas.UpdateSupply, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    supply_db = crud.get_supply_by_id(db, supply.id)

    if supply_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Supply with id: {supply.id} was not found.")

    updated_supply = crud.update_supply_item_quantity(db, supply)

    crud.update_supply_last_modified(db, supply.id)

    return updated_supply


# UPDATE SUPPLY TEMP SENSITIVE
@router.patch("/temp_sensitive/", tags=['Supplies'], response_model=schemas.Supply, status_code=status.HTTP_200_OK)
async def update_supply_name(supply: schemas.UpdateSupply, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    supply_db = crud.get_supply_by_id(db, supply.id)

    if supply_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Supply with id: {supply.id} was not found.")

    updated_supply = crud.update_supply_item_temp_sensitive(db, supply)

    crud.update_supply_last_modified(db, supply.id)

    return updated_supply


# UPDATE RECIEVED BY
@router.patch("/recieved_by/", tags=['Supplies'], response_model=schemas.Supply, status_code=status.HTTP_200_OK)
async def update_supply_temp_sensitive(supply: schemas.UpdateSupply, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    supply_db = crud.get_supply_by_id(db, supply.id)

    if supply_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Supply with id: {supply.id} was not found.")

    updated_supply = crud.update_supply_item_recieved_by(db, supply)

    crud.update_supply_last_modified(db, supply.id)

    return updated_supply


from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from .. import schemas, models
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter()

# GET ALL SUPPLIES
@router.get("/api/supplies", status_code=status.HTTP_200_OK, response_model=List[schemas.Supply], tags=["supplies"])
async def get_supplies(db: Session = Depends(get_db)):
    """Returns all supplies in the database."""

    all_supplies = db.query(models.Supply).all()


    return all_supplies


# GET A SUPPLY ITEM BY ID
@router.get("/api/supplies/{id}",status_code=status.HTTP_200_OK, response_model=schemas.Supply, tags=["supplies"] )
async def get_single_supply(id:int,db: Session = Depends(get_db)):
    """Gets a single supply item from the database based on id."""

    supply = db.query(models.Supply).filter(models.Supply.id == id).first()

    if supply == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Supply Item with the id:{id} was not found.")


    return supply



# CREATE A NEW SUPPLY ITEM
@router.post("/api/supplies",status_code=status.HTTP_201_CREATED, response_model=schemas.Supply, tags=["supplies"])
async def create_new_supply(supply:schemas.CreateSupply, db: Session = Depends(get_db)):
    """Creates a new supply item in the database."""

    new_supply_item = models.Supply(**supply.dict())

    db.add(new_supply_item)
    db.commit()
    db.refresh(new_supply_item)

    return new_supply_item


from fastapi import APIRouter, status, Depends
from typing import List
from .. import schemas, models
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter()

# GET ALL SUPPLIES
@router.get("/api/supplies", status_code=status.HTTP_200_OK, response_model=List[schemas.Supply])
async def get_supplies(db: Session = Depends(get_db)):
    """Returns all supplies in the database."""

    all_supplies = db.query(models.Supply).all()


    return all_supplies


# CREATE A NEW SUPPLY ITEM
@router.post("/api/supplies",status_code=status.HTTP_201_CREATED, response_model=schemas.Supply)
async def create_new_supply(supply:schemas.CreateSupply, db: Session = Depends(get_db)):


    new_supply_item = models.Supply(**supply.dict())

    db.add(new_supply_item)
    db.commit()
    db.refresh(new_supply_item)

    return new_supply_item
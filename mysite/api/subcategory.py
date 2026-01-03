from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models import SubCategory
from mysite.database.schema import (
    SubCategoryInputSchema,
    SubCategoryOutSchema
)

subcategory_router = APIRouter(prefix="/subcategories", tags=['Subcategory CRUB'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@subcategory_router.post("/", response_model=SubCategoryOutSchema)
def create_subcategory(
    subcategory: SubCategoryInputSchema,
    db: Session = Depends(get_db)
):
    sub_db = SubCategory(**subcategory.dict())
    db.add(sub_db)
    db.commit()
    db.refresh(sub_db)
    return sub_db

@subcategory_router.get("/", response_model=List[SubCategoryOutSchema])
def list_subcategories(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()

@subcategory_router.get("/{subcategory_id}/", response_model=SubCategoryOutSchema)
def detail_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db)
):
    sub_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()

    if not sub_db:
        raise HTTPException(
            status_code=400,
            detail="Мындай маалымыт жок"
        )

    return sub_db

@subcategory_router.put('/{subcategory_id}/', response_model=dict)
async def update_subcategory(subcategory_id: int, subcategory: SubCategoryInputSchema,
    db: Session = Depends(get_db)):

    subcategory_db = (db.query(SubCategory).filter(SubCategory.id == subcategory_id).first())

    if not subcategory_db:
        raise HTTPException(detail='Мындай подкатегория жок',status_code=400)

    for subcategory_key, subcategory_value in subcategory.dict().items():
        setattr(subcategory_db, subcategory_key, subcategory_value)

    db.commit()
    db.refresh(subcategory_db)

    return {'message': 'Подкатегория өзгөртүлдү'}


@subcategory_router.delete('/{subcategory_id}/', response_model=dict)
async def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory_db = (db.query(SubCategory).filter(SubCategory.id == subcategory_id).first())

    if not subcategory_db:
        raise HTTPException(detail='Мындай подкатегория жок', status_code=400)

    db.delete(subcategory_db)
    db.commit()
    return {'message': 'Подкатегория өчүрүлдү'}



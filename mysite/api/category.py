from http.client import responses
from typing import List

import category
from email_validator import caching_resolver
from fastapi import APIRouter, Depends, HTTPException
from mako.util import restore__ast
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models import Category
from mysite.database.schema import CategoryInputSchema, CategoryOutSchema

category_router = APIRouter(prefix="/categories", tags=['Category CRUD'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post("/", response_model=CategoryOutSchema)
def create_category(
    category: CategoryInputSchema, db: Session = Depends(get_db)):

    category_db = Category(**category.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.get("/", response_model=List[CategoryOutSchema])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get("/{category_id}/", response_model=CategoryOutSchema)
def detail_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category_db = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category_db:
        raise HTTPException(
            status_code=400,
            detail="Мындай маалымат жок"
        )

    return category_db

@category_router.put('/{category_id}/', response_model=dict)
async def update_category(category_id: int, category: CategoryInputSchema,
                          db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id==category_id).first()
    if not category_db:
        raise HTTPException(detail='мындай категори жок', status_code=400)

    for category_key, category_value in category.dict().items():
        setattr(category_db, category_key, category_value)

        db.commit()
        db.refresh(category_db)
        return {'message':'Категори озгорулду'}


@category_router.delete('/{category_id}/', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(detail='Мындай категору жок', status_code=400)

    db.delete(category_db)
    db.commit()
    return {'message': 'Категори удалить болду'}




from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models import Product
from mysite.database.schema import ProductInputSchema, ProductOutSchema

product_router = APIRouter(prefix="/products", tags=['Product CRUD'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post("/", response_model=ProductOutSchema)
def create_product(
    product: ProductInputSchema,
    db: Session = Depends(get_db)
):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get("/", response_model=List[ProductOutSchema])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get("/{product_id}/", response_model=ProductOutSchema)
def detail_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_db = db.query(Product).filter(Product.id == product_id).first()

    if not product_db:
        raise HTTPException(
            status_code=400,
            detail="Мындай маалымат жок"
        )

    return product_db

@product_router.put('/{product_id}/', response_model=dict)
async def update_product(product_id: int, product: ProductInputSchema,
                          db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()
    if not product_db:
        raise HTTPException(detail='мындай категори жок', status_code=400)

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)

        db.commit()
        db.refresh(product_db)
        return {'message':'Категори озгорулду'}


@product_router.delete('/{product_id}/', response_model=dict)
async def delete_category(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай категору жок', status_code=400)

    db.delete(product_db)
    db.commit()
    return {'message': 'Категори удалить болду'}


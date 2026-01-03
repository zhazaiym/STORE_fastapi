from typing import List
from fastapi import APIRouter, Depends, HTTPException
from mako.util import restore__ast
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models import ProductImage
from mysite.database.schema import (
    ProductImageInputSchema,
    ProductImageOutSchema
)

product_image_router = APIRouter(prefix="/product-images", tags=['Product_image CRUD'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_image_router.post("/", response_model=ProductImageOutSchema)
def create_product_image(
    image: ProductImageInputSchema,
    db: Session = Depends(get_db)
):
    image_db = ProductImage(**image.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db


@product_image_router.get("/", response_model=List[ProductImageOutSchema])
def list_product_images(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()


@product_image_router.get("/{image_id}/", response_model=ProductImageOutSchema)
def detail_product_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    image_db = db.query(ProductImage).filter(
        ProductImage.id == image_id
    ).first()

    if not image_db:
        raise HTTPException(
            status_code=400,
            detail="Мындай маалымат  жок"
        )

    return image_db

@product_image_router.put('/{product_image_id}/', response_model=dict)
async def update_product_image(product_image_id: int, product_image: ProductImageInputSchema,
                               db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id==product_image_id).first()
    if not product_image_db:
        raise HTTPException(detail='мындай продукт жок', status_code=400)

    for product_image_key, product_image_value in product_image.dict().items():
        setattr(product_image_db, product_image_key, product_image_value)

        db.commit()
        db.refresh(product_image_db)
        return {'message':'Продукт озгорулду'}



@product_image_router.delete('/{product_image_id}/',response_model=dict)
async def delete_product_image(product_image_id: int, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image_db:
        raise HTTPException(detail='Мындай продукт жок', status_code=400)

    db.delete(product_image_db)
    db.commit()
    return {'message': 'Категори удалить болду'}

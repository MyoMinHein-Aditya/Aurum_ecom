"""
product_service.py
Business logic for products.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from BackEnd.database.models import Product
from BackEnd.models.product import ProductReq
from typing import List

def get_all_products(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Product]:
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.contains(search) | Product.category.contains(search))
    return query.offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

def create_product(db: Session, product_data: ProductReq) -> Product:
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    db.delete(product)
    db.commit()

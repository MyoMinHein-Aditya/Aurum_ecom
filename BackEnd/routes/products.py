"""
products.py
Product routes.
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from BackEnd.database.connection import get_db
from BackEnd.models.product import ProductReq, ProductResp
from BackEnd.services import product_service
from BackEnd.utils.deps import get_admin_user
from BackEnd.database.models import User

router = APIRouter(tags=["Products"])

@router.get("/", response_model=List[ProductResp])
def get_products(request: Request, skip: int = 0, limit: int = 100, search: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve all products."""
    return product_service.get_all_products(db, skip=skip, limit=limit, search=search)

@router.get("/{product_id}", response_model=ProductResp)
def get_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product by ID."""
    return product_service.get_product_by_id(db, product_id)

@router.post("/", response_model=ProductResp)
def create_product(request: Request, product: ProductReq, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Create a new product (Admin only)."""
    return product_service.create_product(db, product)

@router.delete("/{product_id}", status_code=204)
def delete_product(request: Request, product_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Delete a product (Admin only)."""
    product_service.delete_product(db, product_id)
    return None

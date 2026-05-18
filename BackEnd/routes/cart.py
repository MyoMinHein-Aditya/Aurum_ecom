"""
cart.py
Cart routes.
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from BackEnd.database.connection import get_db
from BackEnd.models.cart import CartItemReq, CartResp, CartItemResp
from BackEnd.services import cart_service
from BackEnd.utils.deps import get_current_user
from BackEnd.database.models import User

router = APIRouter(tags=["Cart"])

@router.get("/", response_model=CartResp)
def get_cart(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve user cart."""
    items = cart_service.get_cart_items(db, current_user.id)
    return {"items": items}

@router.post("/add", response_model=CartItemResp)
def add_to_cart(request: Request, item: CartItemReq, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Add item to cart."""
    return cart_service.add_to_cart(db, current_user.id, item)

@router.delete("/remove/{product_id}", status_code=204)
def remove_from_cart(request: Request, product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Remove item from cart."""
    cart_service.remove_from_cart(db, current_user.id, product_id)
    return None

@router.post("/clear", status_code=204)
def clear_cart(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Clear all items in cart."""
    cart_service.clear_cart(db, current_user.id)
    return None

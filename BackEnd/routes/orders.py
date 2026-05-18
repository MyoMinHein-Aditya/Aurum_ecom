"""
orders.py
Order routes.
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from BackEnd.database.connection import get_db
from BackEnd.models.order import CheckoutReq, OrderResp
from BackEnd.services import order_service
from BackEnd.utils.deps import get_current_user, get_optional_user
from BackEnd.database.models import User

router = APIRouter(tags=["Orders"])

@router.post("/checkout", response_model=OrderResp)
def checkout(request: Request, checkout_data: CheckoutReq, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    """Checkout cart and create an order."""
    user_id = current_user.id if current_user else None
    return order_service.checkout(db, user_id, checkout_data)

@router.get("/", response_model=List[OrderResp])
def get_orders(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all orders for current user."""
    return order_service.get_user_orders(db, current_user.id)

@router.get("/{order_id}", response_model=OrderResp)
def get_order(request: Request, order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get specific order."""
    return order_service.get_order_by_id(db, current_user.id, order_id)

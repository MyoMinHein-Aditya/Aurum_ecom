"""
admin.py
Admin routes.
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from BackEnd.database.connection import get_db
from BackEnd.services import admin_service
from BackEnd.utils.deps import get_admin_user
from BackEnd.database.models import User
from pydantic import BaseModel

router = APIRouter(tags=["Admin"])

class OrderStatusUpdate(BaseModel):
    status: str

@router.get("/dashboard")
def get_dashboard_stats(request: Request, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Get dashboard stats (Admin only)."""
    return admin_service.get_dashboard_stats(db)

@router.get("/orders")
def get_all_orders(request: Request, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Get all orders (Admin only)."""
    # Quick dump for simplicity, but ideally we use OrderResp
    orders = admin_service.get_all_orders(db)
    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "total_amount": o.total_amount,
            "status": o.status,
            "created_at": o.created_at
        } for o in orders
    ]

@router.put("/orders/{order_id}/status")
def update_order_status(request: Request, order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    """Update order status (Admin only)."""
    order = admin_service.update_order_status(db, order_id, status_update.status)
    return {"id": order.id, "status": order.status}

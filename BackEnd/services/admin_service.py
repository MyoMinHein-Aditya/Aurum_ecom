"""
admin_service.py
Business logic for admin dashboard.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from BackEnd.database.models import User, Order, Product
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

def get_dashboard_stats(db: Session):
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0.0
    
    today = datetime.now(timezone.utc).date()
    orders_today = db.query(Order).filter(func.date(Order.created_at) == today).count()
    
    new_users = db.query(User).count() # Just total users for now
    
    low_stock_count = db.query(Product).filter(Product.stock < 5).count()
    
    # Weekly sales (last 7 days)
    weekly_sales = []
    for i in range(7):
        day = today - timedelta(days=6-i)
        day_total = db.query(func.sum(Order.total_amount)).filter(func.date(Order.created_at) == day).scalar() or 0.0
        weekly_sales.append({
            "date": day.strftime("%Y-%m-%d"),
            "amount": day_total
        })
        
    return {
        "total_revenue": total_revenue,
        "orders_today": orders_today,
        "new_users": new_users,
        "low_stock_count": low_stock_count,
        "weekly_sales": weekly_sales
    }

def get_all_orders(db: Session):
    return db.query(Order).order_by(Order.created_at.desc()).all()

def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    db.commit()
    db.refresh(order)
    return order

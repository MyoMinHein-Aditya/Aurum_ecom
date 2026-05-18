"""
order_service.py
Business logic for orders.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from BackEnd.database.models import Order, OrderItem, CartItem, Product
from BackEnd.models.order import CheckoutReq
from typing import List, Optional

def checkout(db: Session, user_id: Optional[int], checkout_data: CheckoutReq) -> Order:
    if user_id is not None:
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    else:
        cart_items = checkout_data.guest_cart_items or []
        if not checkout_data.email:
            raise HTTPException(status_code=400, detail="Email is required for guest checkout")

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Simulated Payment Gateway
    payment_status = "pending"
    if checkout_data.payment_token:
        if checkout_data.payment_token == "tok_fail":
            raise HTTPException(status_code=400, detail="Payment declined")
        payment_status = "paid"
    else:
        # Require payment token for this version
        raise HTTPException(status_code=400, detail="Payment token is required")

    total_amount = 0
    order_items = []
    
    for c_item in cart_items:
        product = db.query(Product).filter(Product.id == c_item.product_id).first()
        if not product or product.stock < c_item.quantity:
            raise HTTPException(status_code=400, detail=f"Product {product.name if product else c_item.product_id} is out of stock")
        
        # Deduct stock
        product.stock -= c_item.quantity
        price = product.price
        total_amount += price * c_item.quantity
        
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=c_item.quantity,
                price=price
            )
        )
        
    new_order = Order(
        user_id=user_id,
        guest_email=checkout_data.email if user_id is None else None,
        address=checkout_data.address,
        payment_status=payment_status,
        total_amount=total_amount,
        status="pending"
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    for o_item in order_items:
        o_item.order_id = new_order.id
        db.add(o_item)
        
    if user_id is not None:
        # Clear cart
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()

    db.commit()
    db.refresh(new_order)
    
    return new_order

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

def get_order_by_id(db: Session, user_id: int, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

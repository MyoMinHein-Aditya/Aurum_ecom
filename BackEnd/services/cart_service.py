"""
cart_service.py
Business logic for user carts.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from BackEnd.database.models import CartItem, Product
from BackEnd.models.cart import CartItemReq
from typing import List

def get_cart_items(db: Session, user_id: int) -> List[CartItem]:
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, item_data: CartItemReq) -> CartItem:
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    existing_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == item_data.product_id).first()
    if existing_item:
        existing_item.quantity += item_data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
        
    new_item = CartItem(user_id=user_id, product_id=item_data.product_id, quantity=item_data.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def remove_from_cart(db: Session, user_id: int, product_id: int):
    item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()
    if item:
        db.delete(item)
        db.commit()

def clear_cart(db: Session, user_id: int):
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()

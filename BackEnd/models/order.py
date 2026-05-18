from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from BackEnd.models.product import ProductResp
from BackEnd.models.cart import CartItemReq

class OrderItemResp(BaseModel):
    id: int
    product: ProductResp
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderResp(BaseModel):
    id: int
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemResp]

    class Config:
        from_attributes = True

class CheckoutReq(BaseModel):
    address: str = Field(..., min_length=5)
    email: Optional[str] = None
    payment_token: Optional[str] = None
    guest_cart_items: Optional[List[CartItemReq]] = None

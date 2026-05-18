from pydantic import BaseModel, Field
from typing import List
from BackEnd.models.product import ProductResp

class CartItemReq(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class CartItemResp(BaseModel):
    id: int
    product: ProductResp
    quantity: int

    class Config:
        from_attributes = True

class CartResp(BaseModel):
    items: List[CartItemResp]

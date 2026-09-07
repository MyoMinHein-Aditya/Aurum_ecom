from pydantic import BaseModel, Field
from typing import Optional

class ProductReq(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(...)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: str = Field(...)
    image_url: Optional[str] = None

class ProductResp(ProductReq):
    id: int

    class Config:
        from_attributes = True

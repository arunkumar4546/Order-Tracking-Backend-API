from pydantic import BaseModel
from app.core.constants import OrderStatus

class OrderCreate(BaseModel):
    item_name: str
    quantity: int

class OrderResponse(BaseModel):
    id: int
    item_name: str
    quantity: int
    status: str

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus



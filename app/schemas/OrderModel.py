from pydantic import BaseModel, Field
from typing import List
from app.schemas.models.Status import Status
from app.schemas.models.OrderItem import OrderItem
from datetime import datetime


class Order(BaseModel):
    customer: str = Field(default=..., description="Покупатель")
    goods: List[OrderItem] = Field(default=..., description="Товары")
    status: Status = Field(default=..., description="Статус заказа")


class OrderUpdate(Order):
    pass


class OrderCreate(Order):
    pass


class OrderResponse(Order):
    id: int = Field(..., description="ID заказа")
    created_at: datetime = Field(..., description="Дата создания")
    total_price: int = Field(..., description="Стоимость за все")

    class Config:
        orm_mode = True

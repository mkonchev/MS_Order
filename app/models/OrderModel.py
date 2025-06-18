from pydantic import BaseModel, Field
from typing import List
from app.models.Status import Status
from datetime import datetime


class OrderCreate(BaseModel):
    customer: str = Field(default=..., description="Покупатель")
    goods: List = Field(default=..., description="Товары")
    status: Status = Field(default=..., description="Статус заказа")


class OrderResponse(OrderCreate):
    id: int = Field(..., description="ID заказа")
    created_at: datetime = Field(..., description="Дата создания")

    class Config:
        orm_mode = True

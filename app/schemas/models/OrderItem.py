from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    item_id: int = Field(..., description="ID товара")
    quantity: int = Field(1, gt=0, description="Количество товара")
    name: str | None = None
    price: int | None = None
    price_at_order: int | None = None

    def __str__(self):
        return super().__str__()


class OrderItemResponce(OrderItem):
    name: str = Field(..., description="Название товара")
    price: int = Field(..., description="Цена за 1")
    total_price: int = Field(..., description="Цена за все")

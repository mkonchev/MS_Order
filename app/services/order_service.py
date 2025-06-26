from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud import order as crud
from app.schemas.OrderModel import Order, OrderUpdate, OrderResponse
import json
import requests

CATALOG_URL = "http://catalog:80"


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order):
        # Получаем информацию о товарах из каталога
        goods_data = []
        for item_id in order.goods:
            try:
                response = requests.get(
                    f"{CATALOG_URL}/{item_id}",
                    timeout=2,
                )
                if response.status_code != 200:
                    continue
                catalog_item = response.json()

                goods_data.append({
                    "id": item_id,
                    "name": catalog_item["name"],
                    "category": catalog_item["category"],
                    "price": catalog_item["price"],
                    "price_at_order": catalog_item["price"]
                })
            except requests.RequestException:
                continue

        order_data = order.model_dump()
        order_data["goods"] = goods_data
        db_order = crud.create_order(self.db, Order(**order_data))

        return self._format_order_response(db_order)

    def get_order(self, order_id: int):
        db_order = crud.get_order(self.db, order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return self._format_order_response(db_order)

    def get_orders(self):
        db_orders = crud.get_orders(self.db)
        return [self._format_order_response(order) for order in db_orders]

    def update_order(self, order_id: int, order: OrderUpdate):
        db_order = crud.update_order(self.db, order_id, order)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return self._format_order_response(db_order)

    def delete_order(self, order_id: int):
        db_order = crud.delete_order(self.db, order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return self._format_order_response(db_order)

    def _format_order_response(self, db_order):
        goods_from_db = []
        if db_order.goods:
            goods_from_db = json.loads(db_order.goods)["items"]

        return OrderResponse(
            id=db_order.id,
            customer=db_order.customer,
            goods=goods_from_db,
            status=db_order.status,
            created_at=db_order.created_at
        )

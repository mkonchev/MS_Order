import json
import requests
import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud import order as crud
from app.schemas.OrderModel import Order, OrderUpdate, OrderResponse
from app.schemas.models.OrderItem import OrderItem


CATALOG_URL = "http://catalog"


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order):
        goods_data = self.get_goods(order)
        order_data = {
            "customer": order.customer,
            "status": order.status.value,
            "goods": json.dumps({
                "items": [{
                    "item_id": item.item_id,
                    "quantity": item.quantity,
                    "name": item.name,
                    "price": item.price,
                    "price_at_order": item.price_at_order
                } for item in goods_data]
            }),
            "created_at": datetime.datetime.now()
        }
        db_order = crud.create_order(self.db, order_data)
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
        goods_data = self.get_goods(order)
        old_order = self.get_order(order_id)
        order_data = {
            "id": order_id,
            "customer": order.customer,
            "status": order.status.value,
            "goods": json.dumps({
                "items": [{
                    "item_id": item.item_id,
                    "quantity": item.quantity,
                    "name": item.name,
                    "price": item.price,
                    "price_at_order": item.price_at_order
                } for item in goods_data]
            }),
            "created_at": old_order.created_at
        }
        db_order = crud.update_order(self.db, order_id, order_data)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return self._format_order_response(db_order)

    def delete_order(self, order_id: int):
        db_order = crud.delete_order(self.db, order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return self._format_order_response(db_order)

    def _format_order_response(self, db_order: Order):
        goods_from_db = []
        if db_order.goods:
            try:
                parsed = json.loads(db_order.goods)
                if isinstance(parsed, list):
                    goods_from_db = parsed
                elif isinstance(parsed, dict) and "items" in parsed:
                    goods_from_db = parsed["items"]
                elif isinstance(parsed, dict) and "goods" in parsed:
                    goods_from_db = parsed["goods"]
            except json.JSONDecodeError as e:
                print(f"Error parsing goods: {e}")

        total_price = sum(
            item.get('price_at_order', 0) or 0
            for item in goods_from_db
            if isinstance(item, dict)
        )

        return OrderResponse(
            id=db_order.id,
            customer=db_order.customer,
            goods=goods_from_db,
            status=db_order.status,
            created_at=db_order.created_at,
            total_price=total_price
        )

    def get_goods(self, order: Order):
        goods_data = []
        for order_item in order.goods:
            try:
                response = requests.get(
                    f"{CATALOG_URL}/catalog/{order_item.item_id}",
                    timeout=2,
                )
                if response.status_code != 200:
                    continue
                catalog_item = response.json()

                goods_data.append(OrderItem(
                    item_id=order_item.item_id,
                    quantity=order_item.quantity,
                    name=catalog_item.get("name"),
                    price=catalog_item.get("price"),
                    price_at_order=(catalog_item.get("price", 0)
                                    * order_item.quantity)
                ))

                print(goods_data)
            except requests.RequestException:
                continue
        return goods_data

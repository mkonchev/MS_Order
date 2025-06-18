import requests
import json
from fastapi import APIRouter, Depends
from app.models.OrderModel import OrderCreate, OrderResponse
from sqlalchemy.orm import Session
from app.database import DBOrders, get_db

from typing import List
# поправить импорты


router = APIRouter(prefix="/orders", tags=["orders"])


# сделать api тонким, всю бизнес-логику в сервисы
@router.post("/", response_model=OrderResponse)
def create_order(item: OrderCreate, db: Session = Depends(get_db)):
    goods_data = []
    for i in item.goods:
        response = requests.get(
            f"http://127.0.0.1:8002/catalog/{i}",
            timeout=2,
        )
        if response.status_code != 200:
            continue
        catalog_item = response.json()

        goods_data.append({
            "id": i,
            "name": catalog_item["name"],
            "category": catalog_item["category"],
            "price": catalog_item["price"],
            # "quantity": item.quantity,
            "price_at_order": catalog_item["price"]
        })

    db_order = DBOrders(
        customer=item.customer,
        goods=json.dumps({"items": goods_data}),
        status=item.status
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    if db_order.goods:
        goods_from_db = json.loads(db_order.goods)["items"]
    return {
        "id": db_order.id,
        "customer": db_order.customer,
        "goods": goods_from_db,
        "status": db_order.status,
        "created_at": db_order.created_at
    }


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(DBOrders).filter(DBOrders.id == order_id).first()

    goods_from_db = []
    if db_order.goods:
        goods_from_db = json.loads(db_order.goods)["items"]

    return {
        "id": db_order.id,
        "customer": db_order.customer,
        "goods": goods_from_db,
        "status": db_order.status,
        "created_at": db_order.created_at
    }


@router.get("/", response_model=List[OrderResponse])
def read_all_items(db: Session = Depends(get_db)):
    db_orders = db.query(DBOrders).all()

    orders_response = []
    for db_order in db_orders:
        goods_from_db = []
        if db_order.goods:
            goods_from_db = json.loads(db_order.goods)["items"]

        orders_response.append({
            "id": db_order.id,
            "customer": db_order.customer,
            "goods": goods_from_db,  # Список товаров
            "status": db_order.status,
            "created_at": db_order.created_at
        })

    return orders_response

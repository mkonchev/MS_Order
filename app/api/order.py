from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.OrderModel import Order, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=OrderResponse)
def create_order(
    order: Order,
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    return service.create_order(order)


@router.get("/", response_model=List[OrderResponse])
def read_orders(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.get_orders()


@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.get_order(order_id)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order: Order,
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    return service.update_order(order_id, order)


@router.delete("/{order_id}", response_model=OrderResponse)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.delete_order(order_id)

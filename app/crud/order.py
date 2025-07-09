from sqlalchemy.orm import Session
from app.db import models
# from app.schemas.OrderModel import OrderUpdate
# import json


def create_order(db: Session, order_data: dict):
    db_order = models.DBOrders(
        customer=order_data["customer"],
        status=order_data["status"],
        goods=order_data["goods"],
        created_at=order_data.get("created_at")
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(models.DBOrders
                    ).filter(
                    models.DBOrders.id == order_id
                    ).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBOrders).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, order_data: dict):
    model_fields = {column.name
                    for column in models.DBOrders.__table__.columns}
    update_data = {k: v for k, v in order_data.items() if k in model_fields}
    db_order = get_order(db, order_id)
    if db_order:
        db.query(models.DBOrders
                 ).filter(
                 models.DBOrders.id == order_id
                 ).update(update_data)

        db.commit()
    return db.query(models.DBOrders
                    ).filter(
                    models.DBOrders.id == order_id
                    ).first()


def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

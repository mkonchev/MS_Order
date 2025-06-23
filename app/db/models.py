from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.orm import declarative_base
from app.schemas.models.Status import Status as StatusEnum
from app.db.database import engine


Base = declarative_base()


class DBOrders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer = Column(String)
    status = Column(Enum(StatusEnum))
    goods = Column(Text)
    # в goods сидит JSON как String
    created_at = Column(DateTime, default=datetime.now)


Base.metadata.create_all(bind=engine)

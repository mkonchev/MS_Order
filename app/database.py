from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, \
                        String, Text, Enum, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models.Status import Status as StatusEnum


# Подключение к SQLite (файл создастся автоматически)
SQLALCHEMY_DATABASE_URL = "sqlite:///./orders.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False}
                       )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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


# лучше вынести в отдельный слой
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

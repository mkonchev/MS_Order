from fastapi import FastAPI
from app.api.endpoints import router as order_router

app = FastAPI()

app.include_router(order_router)

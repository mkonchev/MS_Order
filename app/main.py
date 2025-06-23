from fastapi import FastAPI
from app.api.order import router as order_router

app = FastAPI()

app.include_router(order_router)


@app.get("/")
def health_check():
    return {"message": "Order works"}

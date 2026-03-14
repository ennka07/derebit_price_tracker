from fastapi import APIRouter
from app.api.v1.endpoints import prices

api_router = APIRouter()

# Подключение роутеров
api_router.include_router(prices.router)
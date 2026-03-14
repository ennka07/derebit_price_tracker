from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class PriceRecordBase(BaseModel):
    """Базовая схема для записи о цене."""

    ticker: str = Field(..., min_length=1, max_length=20, description="Тикер валюты")
    price: float = Field(..., gt=0, description="Индексная цена в USD")
    timestamp: int = Field(..., gt=0, description="UNIX-время записи цены")


class PriceRecordCreate(PriceRecordBase):
    """Схема для создания записи о цене."""
    pass


class PriceRecordResponse(PriceRecordBase):
    """Схема ответа с данными о цене."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Первичный ключ записи")


class PriceRecordListResponse(BaseModel):
    """Схема ответа со списком записей о ценах."""

    total: int = Field(description="Общее количество записей")
    items: List[PriceRecordResponse] = Field(default_factory=list, description="Список записей")
import time
from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.domain.schemas import PriceRecordResponse, PriceRecordListResponse
from app.infrastructure.database.repository import PriceRepository

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get(
    "/all",
    response_model=PriceRecordListResponse,
    summary="Получение всех сохраненных данных по указанной валюте",
    description="Возвращает все записи о ценах для указанного тикера. "
                "Результаты отсортированы по времени (новые сначала)."
)
def get_all_prices(
        ticker: Literal["btc_usd", "eth_usd"] = Query(...,
                                                      description="Тикер валюты (обязательный параметр)"),
        limit: int = Query(100, ge=1, le=1000,
                           description="Максимальное количество записей"),
        db: Session = Depends(get_db)
) -> PriceRecordListResponse:
    """Получение всех сохраненных данных по указанной валюте.

    Args:
        ticker: Тикер валюты (btc_usd или eth_usd) - обязательный параметр
        limit: Максимальное количество записей (по умолчанию 100)
        db: Сессия базы данных

    Returns:
        Список записей о ценах с общим количеством
    """
    repo = PriceRepository(db)
    records = repo.get_all_by_ticker(ticker=ticker, limit=limit)

    return PriceRecordListResponse(
        total=len(records),
        items=[PriceRecordResponse.model_validate(r) for r in records]
    )


@router.get(
    "/latest",
    response_model=PriceRecordResponse,
    summary="Получение последней цены валюты",
    description="Возвращает последнюю сохраненную цену для указанного тикера."
)
def get_latest_price(
        ticker: Literal["btc_usd", "eth_usd"] = Query(...,
                                                      description="Тикер валюты (обязательный параметр)"),
        db: Session = Depends(get_db)
) -> PriceRecordResponse:
    """Получение последней цены валюты.

    Args:
        ticker: Тикер валюты (btc_usd или eth_usd) - обязательный параметр
        db: Сессия базы данных

    Returns:
        Последняя запись о цене

    Raises:
        HTTPException: Если записей для данного тикера не найдено
    """
    repo = PriceRepository(db)
    record = repo.get_latest(ticker=ticker)

    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"No price records found for ticker: {ticker}"
        )

    return PriceRecordResponse.model_validate(record)


@router.get(
    "/range",
    response_model=PriceRecordListResponse,
    summary="Получение цены валюты с фильтром по дате",
    description="Возвращает записи о ценах для указанного тикера в заданном диапазоне времени."
)
def get_prices_by_date_range(
        ticker: Literal["btc_usd", "eth_usd"] = Query(
            ...,
            description="Тикер валюты (обязательный параметр)"
        ),
        start_timestamp: Optional[int] = Query(
            None,
            gt=0,
            description="Начало диапазона (UNIX timestamp) - необязательный"
        ),
        end_timestamp: Optional[int] = Query(
            None,
            gt=0,
            description="Конец диапазона (UNIX timestamp) - необязательный"
        ),
        limit: int = Query(100, ge=1, le=1000,
                           description="Максимальное количество записей"),
        db: Session = Depends(get_db)
) -> PriceRecordListResponse:
    """Получение цены валюты с фильтром по дате.

    Args:
        ticker: Тикер валюты (btc_usd или eth_usd) - обязательный параметр
        start_timestamp: Начало диапазона (UNIX timestamp) - необязательный
        end_timestamp: Конец диапазона (UNIX timestamp) - необязательный
        limit: Максимальное количество записей (по умолчанию 100)
        db: Сессия базы данных

    Returns:
        Список записей о ценах в заданном диапазоне

    Raises:
        HTTPException: Если start_timestamp больше end_timestamp
    """
    # Валидация: если оба параметра указаны, проверяем диапазон
    if start_timestamp is not None and end_timestamp is not None:
        if start_timestamp > end_timestamp:
            raise HTTPException(
                status_code=400,
                detail="start_timestamp must be less than or equal to end_timestamp"
            )

    repo = PriceRepository(db)

    # Если диапазон не указан - получаем все записи по тикеру
    if start_timestamp is None and end_timestamp is None:
        records = repo.get_all_by_ticker(ticker=ticker, limit=limit)
    else:
        # Если указан только один из параметров, используем дефолтные значения
        if start_timestamp is None:
            start_timestamp = 0  # С начала времён
        if end_timestamp is None:
            end_timestamp = int(time.time())  # До текущего момента

        records = repo.get_by_date_range(
            ticker=ticker,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            limit=limit
        )

    return PriceRecordListResponse(
        total=len(records),
        items=[PriceRecordResponse.model_validate(r) for r in records]
    )

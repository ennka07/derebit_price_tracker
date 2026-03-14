from app.infrastructure.celery.config import celery_app
from app.core.config import settings
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.database.repository import PriceRepository
from app.domain.schemas import PriceRecordCreate
import time
from app.infrastructure.deribit.index_price import fetch_index_price
from app.infrastructure.database.session import SyncSessionLocal

# Список тикеров для сбора
TICKERS_TO_COLLECT = ["btc_usd", "eth_usd"]


@celery_app.task(name="collect_prices", bind=True, max_retries=3)
def collect_prices_task(self):
    """Задача Celery для сбора цен по всем тикерам.

    Выполняется каждую минуту через Celery Beat.
    При ошибке делает до 3 повторных попыток.
    """
    results = []

    for ticker in TICKERS_TO_COLLECT:
        try:
            price_data = fetch_index_price(ticker)

            db = SyncSessionLocal()
            repo = PriceRepository(db)

            # 3. Готовим данные для сохранения
            record_data = PriceRecordCreate(
                ticker=ticker,
                price=price_data["index_price"],
                timestamp=int(time.time()),  # Текущий UNIX timestamp
            )

            # 4. Сохраняем в БД
            record = repo.create(record_data)

            results.append({
                "ticker": ticker,
                "status": "success",
                "data": price_data,
                "record_id": record.id
            })
        except Exception as exc:
            # Логирование ошибки (можно добавить logger)
            print(f"Failed to collect {ticker}: {exc}")
            # Повторная попытка через 30 секунд при ошибке
            raise self.retry(exc=exc, countdown=30)
        finally:
            if db:
                db.close()

    return {"collected": len(results), "results": results}

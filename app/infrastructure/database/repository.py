from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.schemas import PriceRecordCreate
from app.infrastructure.database.models import PriceRecord


class PriceRepository:
    """Репозиторий для работы с записями о ценах."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: PriceRecordCreate) -> PriceRecord:
        """Создаёт новую запись о цене."""
        record = PriceRecord(
            ticker=data.ticker,
            price=data.price,
            timestamp=data.timestamp,
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)  # ← Важно: загружает id после commit
        return record

    def get_all_by_ticker(self, ticker: str, limit: int = 100) -> List[
        PriceRecord]:
        """Получает все записи по тикеру."""
        return (
            self.session.query(PriceRecord)
            .filter(PriceRecord.ticker == ticker)
            .order_by(PriceRecord.timestamp.desc())
            .limit(limit)
            .all()
        )

    def get_latest(self, ticker: str) -> Optional[PriceRecord]:
        """Получает последнюю запись по тикеру."""
        return (
            self.session.query(PriceRecord)
            .filter(PriceRecord.ticker == ticker)
            .order_by(PriceRecord.timestamp.desc())
            .first()
        )

    def get_by_date_range(
            self,
            ticker: str,
            start_timestamp: int,
            end_timestamp: int,
            limit: int = 100,
    ) -> List[PriceRecord]:
        """Получает записи по диапазону времени."""
        return (
            self.session.query(PriceRecord)
            .filter(
                PriceRecord.ticker == ticker,
                PriceRecord.timestamp >= start_timestamp,
                PriceRecord.timestamp <= end_timestamp,
            )
            .order_by(PriceRecord.timestamp.desc())
            .limit(limit)
            .all()
        )

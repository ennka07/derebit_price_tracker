from sqlalchemy import Column, Integer, String, BigInteger, Numeric

from app.infrastructure.database.session import Base


class PriceRecord(Base):
    """Модель записи о цене криптовалюты.

    Хранит исторические данные об индексных ценах
    с биржи Deribit для BTC и ETH.
    """

    __tablename__ = "price_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(20), nullable=False, index=True)
    price = Column(Numeric(20, 2), nullable=False)
    timestamp = Column(BigInteger, nullable=False, index=True)

    def __repr__(self) -> str:
        """Строковое представление объекта для отладки."""
        return (
            f"<PriceRecord(id={self.id}, ticker={self.ticker}, "
            f"price={self.price}, timestamp={self.timestamp})>"
        )

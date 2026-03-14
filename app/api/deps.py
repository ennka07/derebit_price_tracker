from sqlalchemy.orm import Session
from app.infrastructure.database.session import SyncSessionLocal


def get_db() -> Session:
    """Получает сессию базы данных.

    Используется как зависимость в FastAPI эндпоинтах.
    """
    db = SyncSessionLocal()
    try:
        return db
    finally:
        db.close()
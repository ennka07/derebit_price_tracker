from celery import Celery
from app.core.config import settings

# Создаём экземпляр Celery
celery_app = Celery(
    "deribit_collector",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.infrastructure.celery.tasks"]
)

# Настройки по умолчанию
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Настройки для продакшена (опционально)
    task_track_started=True,
    task_time_limit=300,  # 5 минут максимум на задачу
)

# Расписание периодических задач
celery_app.conf.beat_schedule = {
    "collect-prices-every-minute": {
        "task": "collect_prices",
        "schedule": 60.0,  # Запуск каждые 60 секунд
        "args": (),
        "kwargs": {},
    },
}
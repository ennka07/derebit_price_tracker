from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения.

    Загружает значения из переменных окружения или .env файла.
    """

    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        env_nested_max_split=1,
        env_file=Path(__file__).parents[2] / ".env"
    )

    # Celery и Redis
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    # Postgres
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_db: str = "deribit_prices"

    @property
    def database_url(self) -> str:
        """Формирует URL подключения к PostgreSQL.

        Return:
            Строка подключения в формате postgresql://user:pass@host:port/db
        """
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # python -c "from app.infrastructure.database.session import init_db"
    # # Deribit API
    # deribit_base_url: str = "https://deribit.com/api/v2"
    # deribit_timeout: int = 10
    #
    # # Тикеры для сбора
    # collect_tickers: str = "btc_usd,eth_usd"


settings = Settings()

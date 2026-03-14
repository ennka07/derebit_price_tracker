import asyncio

from app.infrastructure.database.session import init_db


async def main():
    """Точка входа для асинхронной инициализации."""
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())

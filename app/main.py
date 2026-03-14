from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="Deribit Price Collector",
    version="0.1.0",
    description="Сервис для сбора и хранения цен криптовалют с биржи Deribit"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """
    Эндпоинт для проверки работоспособности сервиса.

    Возвращает базовый статус работы приложения.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

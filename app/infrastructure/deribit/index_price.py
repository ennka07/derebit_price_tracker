import requests

DERIBIT_BASE_URL = "https://deribit.com/api/v2"
VALID_TICKERS = ("btc_usd", "eth_usd")
REQUEST_TIMEOUT = 10


def fetch_index_price(index_name: str) -> dict:
    """Получает индексную цену с биржи Deribit.

    Чистая функция без зависимостей от фреймворков.
    Может использоваться в FastAPI, Celery, тестах, скриптах.

    Args:
        index_name: Название индекса (btc_usd или eth_usd)

    Returns:
        Словарь с ценовыми данными

    Raises:
        ValueError: если index_name не из списка допустимых
        requests.RequestException: при ошибке сетевого запроса
    """
    # Валидация для использования вне FastAPI
    if index_name not in VALID_TICKERS:
        raise ValueError(
            f"Invalid ticker: {index_name}. Must be one of {VALID_TICKERS}")

    url = f"{DERIBIT_BASE_URL}/public/get_index_price"
    params = {"index_name": index_name}

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    data = response.json()

    # Проверка на ошибки в формате JSON-RPC
    if "error" in data:
        raise RuntimeError(
            f"Deribit API error: {data['error'].get('message', 'Unknown error')}")

    result = data.get("result", {})
    return {
        "ticker": index_name,
        "index_price": result.get("index_price"),
        "estimated_delivery_price": result.get("estimated_delivery_price")
    }

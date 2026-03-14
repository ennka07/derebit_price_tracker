# Используем легкий образ с Python
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Отключаем буферизацию вывода (чтобы логи были видны сразу)
ENV PYTHONUNBUFFERED=1

# Команда по умолчанию (переопределяется в docker-compose)
CMD ["python", "app/main.py"]
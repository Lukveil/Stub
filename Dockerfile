# Используем официальный Python образ как базовый
FROM python:3.12.5-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
ADD pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости
RUN poetry install --no-dev

# Копируем оставшиеся файлы проекта
ADD . /app

# Открываем порт для Flask приложения
EXPOSE 5000

# Запускаем приложение
ENTRYPOINT ["poetry", "run", "python", "main.py", "--kafka-broker", "localhost:8083", "--kafka-topic", "topic", "--timeout", "0.1"]

#CMD ["poetry", "run", "python", "main.py", "--kafka-broker", "localhost:8083", "--kafka-topic", "topic", "--timeout", "0.1"]

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

# Запускаем приложение
# неизменяемые
ENTRYPOINT ["poetry", "run", "python", "main.py"]
# изменяемые
CMD ["--kafka-broker", "kafka4:9093", "--kafka-topic", "group4", "--timeout", "0.1"]
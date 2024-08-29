from enum import Enum
from re import sub
from typing import Final
from time import sleep

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from logging import (
    DEBUG, basicConfig, FileHandler,
    StreamHandler, getLogger, Formatter
)
from argparse import ArgumentParser


class AnsiColor(Enum):
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    UNDERLINE = "\x1b[4m"
    REVERSED = "\x1b[7m"
    HIDDEN = "\x1b[8m"
    STRIKETHROUGH = "\x1b[9m"

    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"

    BLACK_BACKGROUND = "\x1b[40m"
    RED_BACKGROUND = "\x1b[41m"
    GREEN_BACKGROUND = "\x1b[42m"
    YELLOW_BACKGROUND = "\x1b[43m"
    BLUE_BACKGROUND = "\x1b[44m"
    MAGENTA_BACKGROUND = "\x1b[45m"
    CYAN_BACKGROUND = "\x1b[46m"
    WHITE_BACKGROUND = "\x1b[47m"


class RemoveColorFormatter(Formatter):
    def format(self, record):
        # Удаление ANSI управляющих кодов
        message = super().format(record)
        return sub(r'\x1b\[[0-9;]*m', '', message)

class Message(BaseModel):
    message: str

# Настройка логирования
LOG_FILENAME: Final[str] = './app.log'
handler = FileHandler(LOG_FILENAME, encoding='utf-8')
handler.setFormatter(RemoveColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
basicConfig(
    level=DEBUG,
    handlers=[
        handler,
        StreamHandler()
    ]
)
logger = getLogger(__name__)


def create_app(kafka_broker: str, kafka_topic: str, timeout:int) -> FastAPI:
    app = FastAPI()

    # Используем переданные аргументы
    # const
    KAFKA_BROKER: Final[str] = kafka_broker
    KAFKA_TOPIC: Final[str] = kafka_topic
    TIMEOUT: Final[float] = timeout
    MAX_WAIT: Final[float] = 0.1

    # Настройки Kafka
    producer = Producer({
        'bootstrap.servers': KAFKA_BROKER,
        'acks': 'all',
        'batch.size': 16384,  # 16 KB
        'linger.ms': 50,  # 50 миллисекунд ожидания
    })
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'kafka_mock_group',
        'auto.offset.reset': 'latest',
        'request.timeout.ms': 200,  # Таймаут запроса
        'delivery.timeout.ms': 200  # Таймаут доставки
    })
    consumer.subscribe([KAFKA_TOPIC])

    @app.post("/send")
    async def send_message(msg: Message):
        try:
            # Отправляем сообщение в Kafka
            logger.info(f'{AnsiColor.YELLOW.value}Sending message to Kafka: {msg.message}{AnsiColor.RESET.value}')
            producer.produce(kafka_topic, value=msg.message)
            logger.info(f'{AnsiColor.YELLOW.value}Message produced: {msg.message}{AnsiColor.RESET.value}')
            try:
                # Метод flush() блокирует выполнение программы до тех пор, пока все сообщения не будут отправлены и подтверждены.
                producer.flush(timeout=MAX_WAIT)
            except KafkaException as e:
                logger.error(f"{AnsiColor.RED.value}Flush error: {e}{AnsiColor.RESET.value}")

            logger.info(f'{AnsiColor.YELLOW.value}Producer flushed: {msg.message}{AnsiColor.RESET.value}')
            return {"status": "Message sent"}
        except KafkaException as e:
            logger.error(f'Kafka exception: {e}')
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/receive")
    async def receive_message():
        try:
            try:
                sleep(TIMEOUT)
                logger.info(f'{AnsiColor.GREEN.value}sleep... {TIMEOUT} sec.{AnsiColor.RESET.value}')
            except OSError as e:
                logger.error(f'{AnsiColor.RED.value}Interrupting a system call: {e}{AnsiColor.RESET.value}')
            # Получаем последнее сообщение из Kafka
            msg = consumer.poll(timeout=TIMEOUT)  # конвертируем миллисекунды в секунды для тайм-аута
            if msg is None:
                logger.info(f'{AnsiColor.GREEN.value}Message received: {msg}{AnsiColor.RESET.value}')
                raise HTTPException(status_code=404, detail="No message available")
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    raise HTTPException(status_code=404, detail="No new messages")
                else:
                    raise KafkaException(msg.error())
            return {"message": msg.value().decode('utf-8')}
        except KafkaException as e:
            logger.error(f'Kafka exception: {e}')
            raise HTTPException(status_code=500, detail=str(e))

    return app


def main():
    parser = ArgumentParser(description='Run a FastAPI application with Kafka integration.')
    parser.add_argument('--kafka-broker', type=str, required=True, help='Kafka broker address')
    parser.add_argument('--kafka-topic', type=str, required=True, help='Kafka topic to use')
    parser.add_argument('--timeout', type=float, required=True, help='Timeout (milliseconds)')
    args = parser.parse_args()

    app = create_app(args.kafka_broker, args.kafka_topic, args.timeout)

    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="debug")


if __name__ == '__main__':
    main()

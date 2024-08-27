from logging import (
    DEBUG, Formatter, FileHandler,
    StreamHandler, basicConfig, getLogger
)
from argparse import ArgumentParser
from re import sub
from typing import Final
from enum import Enum
from time import sleep

from dataclasses import dataclass  # develop...

from flask import Flask, request, jsonify, Response, Request
from confluent_kafka import Producer, Consumer, KafkaException


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


# @dataclass
# class RequestDTO:
#     _message: str
#
#     @setter
#     def message(self, message:str):
#         _message = message
#
#
# @dataclass
# class ResponseDTO:
#     _message: str


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


# develop...
def logger_colored(text, color):
    print(f"{color.value}{text}{AnsiColor.RESET.value}")


def create_app(kafka_broker: str, kafka_topic: str, timeout: int) -> Flask:
    """
    Main app

    :return: Flask app
    """
    logger.info(f'{AnsiColor.BLUE_BACKGROUND.value}App start{AnsiColor.RESET.value}')
    app = Flask(__name__)

    # Настройки Kafka
    # Используем переданные аргументы
    # const
    KAFKA_BROKER: Final[str] = kafka_broker
    KAFKA_TOPIC: Final[str] = kafka_topic
    TIMEOUT: Final[float] = timeout
    MAX_WAIT: Final[float] = 0.5

    # Создание продюсера Kafka
    producer = Producer({
        'bootstrap.servers': KAFKA_BROKER,
        'acks': 'all',
        'batch.size': 16384,  # 16 KB
        'linger.ms': 50,  # 50 миллисекунд ожидания
    })

    # Создание консюмера Kafka
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'kafka_mock_group',
        'auto.offset.reset': 'latest',
        'request.timeout.ms': 200,  # Таймаут запроса
        'delivery.timeout.ms': 200  # Таймаут доставки
    })
    # подписываемся на топик
    consumer.subscribe([KAFKA_TOPIC])

    @app.route('/send', methods=['POST'])
    def send_message()-> tuple[request, int]:
        """
        Отправляет сообщение в Kafka и возвращает статус выполнения.

        description:
        Функция `send_message` предназначена для обработки POST-запросов на маршрут `/send`. Она извлекает сообщение из тела запроса,
        отправляет его в Kafka-поток и возвращает соответствующий ответ в формате JSON. Также функция обрабатывает ошибки и возвращает
        соответствующие HTTP-статусы.

        Вот что возвращает функция `send_message`:

        1. **Если сообщение не предоставлено**:
           - Возвращает JSON-объект с ключом `error` и значением `'No message provided'`.
           - Возвращает HTTP-статус 400 (Bad Request).

        2. **Если сообщение успешно отправлено**:
           - Возвращает JSON-объект с ключом `status` и значением `'Message sent'`.
           - Возвращает HTTP-статус 200 (OK).

        3. **Если происходит исключение `KafkaException`**:
           - Возвращает JSON-объект с ключом `error` и значением исключения в виде строки (`str(e)`).
           - Возвращает HTTP-статус 500 (Internal Server Error).

        Таким образом, функция возвращает кортеж из двух элементов: JSON-объекта и HTTP-статуса.
        Тип возвращаемого значения обозначается как `tuple[Response, int]`,
        где `Response` — это объект, возвращаемый функцией `jsonify`, а `int` — это HTTP-статус.
        :return: tuple[Response, int]
        """
        try:
            message = request.json.get('message')
            if not message:
                logger.error(f'{AnsiColor.RED.value}error: No message provided{AnsiColor.RESET.value}')
                return jsonify({'error': 'No message provided'}), 400

            logger.info(f'{AnsiColor.YELLOW.value}Sending message to Kafka: {message}{AnsiColor.RESET.value}')
            producer.produce(KAFKA_TOPIC, value=message)
            logger.info(f'{AnsiColor.YELLOW.value}Message produced: {message}{AnsiColor.RESET.value}')
            try:
                producer.flush(timeout=MAX_WAIT)
            except KafkaException as e:
                logger.error(f"{AnsiColor.RED.value}Flush error: {e}{AnsiColor.RESET.value}")
            logger.info(f'{AnsiColor.YELLOW.value}Producer flushed: {message}{AnsiColor.RESET.value}')

            return jsonify({'status': 'Message sent'}), 200
        except KafkaException as e:
            logger.error(f'{AnsiColor.RED.value}Kafka exception: {e}{AnsiColor.RESET.value}')
            return jsonify({'error': str(e)}), 500

    @app.route('/receive', methods=['GET'])
    def receive_message() -> tuple[Response, int]:
        """
        Принимает сообщение и выводит

        description:
        Функция `receive_message` в коде предназначена для получения сообщения от потребителя Kafka и
        возврата его в формате JSON. Она также обрабатывает ошибки и возвращает соответствующие HTTP-статусы.

        Вот что возвращает функция `receive_message`:

        1. **Если сообщение не получено (`msg` равно `None`)**:
           - Возвращает JSON-объект с ключом `error` и значением `'No message available'`.
           - Возвращает HTTP-статус 404 (Not Found).

        2. **Если сообщение успешно получено**:
           - Возвращает JSON-объект с ключом `message` и значением, декодированным из байтов в строку (`msg.value().decode('utf-8')`).
           - Возвращает HTTP-статус 200 (OK).

        3. **Если происходит исключение `KafkaException`**:
           - Возвращает JSON-объект с ключом `error` и значением исключения в виде строки (`str(e)`).
           - Возвращает HTTP-статус 500 (Internal Server Error).

        Таким образом, функция возвращает кортеж из двух элементов: JSON-объекта и HTTP-статуса.
        Тип возвращаемого значения можно обозначить как `tuple[Response, int]`,
        где `Response` — это объект, возвращаемый функцией `jsonify`, а `int` — это HTTP-статус.
        :return: tuple[Response, int]
        """
        try:
            try:
                sleep(TIMEOUT)
                logger.info(f'{AnsiColor.GREEN.value}sleep... {TIMEOUT} sec.{AnsiColor.RESET.value}')
            except OSError as e:
                logger.error(f'{AnsiColor.RED.value}Interrupting a system call: {e}{AnsiColor.RESET.value}')

            msg = consumer.poll(timeout=MAX_WAIT)

            if msg is None:
                logger.info(f'{AnsiColor.GREEN.value}Message received: {msg}{AnsiColor.RESET.value}')
                return jsonify({'error': 'No message available'}), 404

            logger.info(f'Message received: {msg.value().decode('utf-8')}')
            return jsonify({'message': msg.value().decode('utf-8')}), 200
        except KafkaException as e:
            logger.error(f'{AnsiColor.RED.value}Kafka exception: {e}{AnsiColor.RESET.value}')
            return jsonify({'error': str(e)}), 500

    return app


def main() -> None:
    """
    Главная функция

    :return: None
    """
    # Парсер командной строки
    parser = ArgumentParser(description='Run a Flask application with Kafka integration.')
    parser.add_argument('--kafka-broker', type=str, required=True, help='Kafka broker address')
    parser.add_argument('--kafka-topic', type=str, required=True, help='Kafka topic to use')
    parser.add_argument('--timeout', type=float, required=True, help='Timeout(seconds) receive message')
    parser.add_argument('--port', type=int, required=True, help='Port')
    # Флаг --debug будет True, если указан
    parser.add_argument('--debug',  action='store_true', help='Debug level on')

    args = parser.parse_args()

    # Создание и запуск Main aoo с аргументами
    app = create_app(args.kafka_broker, args.kafka_topic, args.timeout)
    logger.info(f'{AnsiColor.GREEN.value}Debug level: {args.debug}{AnsiColor.RESET.value}')
    app.run(debug=args.debug, host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()

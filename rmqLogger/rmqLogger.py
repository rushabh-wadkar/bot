import logging
import pika
import constants
import json


class RMQLogger:
    def __init__(self, exchange_name='logs', log_level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Set up logging formatter
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        formatter = logging.Formatter(
            '[%(levelname)s] [%(asctime)s] %(message)s')

        # Set up RMQ connection and channel
        credentials = pika.PlainCredentials(
            constants.RMQ_USERNAME, constants.RMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(constants.RMQ_HOST, credentials=credentials, heartbeat=0))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type='fanout')
        self.channel.queue_declare(
            queue=constants.LOGS_QUEUE_NAME, durable=True)
        self.channel.queue_bind(
            exchange=exchange_name, queue=constants.LOGS_QUEUE_NAME, routing_key=constants.LOGS_QUEUE_NAME)

        # Set up logging handler
        handler = RMQHandler(self.channel, exchange_name)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)


class RMQHandler(logging.Handler):
    def __init__(self, channel, exchange_name='logs'):
        super().__init__()
        self.channel = channel
        self.exchange_name = exchange_name

    def emit(self, record):
        log_message = self.format(record)
        log_level = record.levelname
        obj = {
            "level": log_level,
            "message": log_message
        }

        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=constants.LOGS_QUEUE_NAME,
            body=json.dumps(obj),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

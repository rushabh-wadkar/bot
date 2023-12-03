import pika
import json
import sys
import os
import traceback
from datetime import datetime
import pymongo
import constants

credentials = pika.PlainCredentials(
    constants.RMQ_USERNAME, constants.RMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(constants.RMQ_HOST, credentials=credentials, heartbeat=0))

channel = connection.channel()
channel.queue_declare(queue=constants.LOGS_QUEUE_NAME, durable=True)

conn = pymongo.MongoClient(constants.DB_HOST, port=constants.DB_PORT, username=constants.DB_USERNAME,
                           password=constants.DB_PASSWORD, authSource=constants.DB_DATABASE_NAME, authMechanism='SCRAM-SHA-256')
# conn = pymongo.MongoClient("mongodb://dev:admindev@192.168.0.141:27017/aidb")
db = conn[constants.DB_DATABASE_NAME]
logs_collection = db[constants.DB_TABLE_LOGS]

# logs_collection.create_index([("id", 1)], unique=True)
max_id = None


def get_next_id():
    global max_id

    if max_id == None:
        # Find the maximum ID in the collection and increment it
        result = logs_collection.find_one(
            sort=[("id", -1)], projection={"_id": 0, "id": 1})
        max_id = result["id"] if result and "id" in result else 0

    max_id = max_id + 1
    return max_id


def handle_logs_callback(ch, method, properties, body):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        log = json.loads(body)

        log_msg = log["message"]
        level = log["level"]
        next_id = get_next_id()
        obj = {
            "id": next_id,
            "timestamp": now,
            "log": log_msg,
            "type": level
        }
        logs_collection.insert_one(obj)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as err:
        error_message = traceback.format_exc()
        err = f'Error: {str(err)} Stack: {error_message}'
        print(err)


def consume_logs_channel(channel):
    channel.basic_consume(
        queue=constants.LOGS_QUEUE_NAME, on_message_callback=handle_logs_callback
    )


def run():
    print("Starting logger consumer ")
    consume_logs_channel(channel)

    print("Waiting for logs messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        run()
    except Exception as err:
        # Close DB
        connection.close()
        error_message = traceback.format_exc()
        err = f'Error: {str(err)} Stack: {error_message}'
        print(err)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

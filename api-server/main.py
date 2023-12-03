import subprocess
from nanoid import generate
from fastapi import FastAPI, HTTPException, Query, Request
from pymongo import MongoClient
from typing import List
from datetime import datetime
import constants
import json
import time
import pika
import traceback
from pydantic import BaseModel
from rmqLogger import RMQLogger
import pymongo
import demoji
import bleach
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins (you might want to restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger = RMQLogger()

credentials = pika.PlainCredentials(
    constants.RMQ_USERNAME, constants.RMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(constants.RMQ_HOST, credentials=credentials, heartbeat=0))
channel = connection.channel()
channel.queue_declare(
    queue=constants.ASK_QUESTION_QUEUE_NAME, durable=True)
channel.queue_declare(
    queue=constants.LOGS_QUEUE_NAME, durable=True)
channel.exchange_declare(
    exchange=constants.MODEL_CONFIG_EXCHANGE, exchange_type='fanout')


logger.info("Configuring DB in api-server")
conn = pymongo.MongoClient(constants.DB_HOST, port=constants.DB_PORT, username=constants.DB_USERNAME,
                           password=constants.DB_PASSWORD, authSource=constants.DB_DATABASE_NAME, authMechanism='SCRAM-SHA-256')
# conn = pymongo.MongoClient("mongodb://dev:admindev@192.168.0.141:27017/aidb")
db = conn[constants.DB_DATABASE_NAME]
logs_collection = db[constants.DB_TABLE_LOGS]
logger.info("Db configuration in api-server successfull..")


class ModelObjectUpdateClass(BaseModel):
    value: str


def process_user_question_with_emojis(question):
    # Extract emojis
    # emojis = [c for c in question if c in emoji.UNICODE_EMOJI]

    # Remove emojis from the original question
    # sanitized_question = re.sub(emoji.get_emoji_regexp(), '', question).strip()
    sanitized_question = demoji.replace(question, '').strip()

    # Sanitize HTML/tags
    sanitized_question = bleach.clean(sanitized_question, tags=[], strip=True)

    sanitized_question = sanitized_question.replace("\n", ".")
    sanitized_question = sanitized_question.replace("\t", " ")

    return sanitized_question


@app.get("/api")
def root():
    logger.info("Someone reached the API server")
    return {"msg": "You've reached the api server."}


@app.get("/api/webhook")
def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
):
    """
    Verify webhook for Facebook Messenger.
    """
    # Replace "YOUR_VERIFY_TOKEN" with your actual verify token
    verify_token = constants.VERIFY_TOKEN

    # Check if the mode and token sent are correct
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        # Respond with 200 OK and challenge token from the request
        logger.info("WEBHOOK_VERIFIED")
        return hub_challenge
    else:
        logger.error(
            f"Forbidden request for webhook /api/webhook endpoint (hub_mode: {hub_mode} hub_verify_token: {hub_verify_token} hub_challenge: {hub_challenge})")
        # Responds with '403 Forbidden' if verify tokens do not match
        raise HTTPException(status_code=403, detail="Forbidden")


@app.post("/api/model/update")
def update_model(data: ModelObjectUpdateClass, status=201):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        req_data = {
            "req_id": generate(),
            "req_timestamp": now,
        }
        json_value = data.model_dump()
        logger.info(
            f"Request to update the model with parameters: {json.dumps(json_value)}")
        custom_obj = {
            "req": req_data,
            "value": json_value
        }
        channel.basic_publish(exchange=constants.MODEL_CONFIG_EXCHANGE, routing_key='', body=json.dumps(custom_obj), properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),)
    except Exception as err:
        error_message = traceback.format_exc()
        err = f'Error in /api/model/update: {str(err)} Stack: {error_message} [Req: {req_data}]'
        logger.error(err)
        return {"error": f"err"}

    return {"response": "ok"}


def process_whatsapp_msg(data):
    if data.get("object") == "whatsapp_business_account":
        entry = data.get("entry", [])
        if entry and entry[0].get("changes"):
            changes = entry[0]["changes"][0]
            if changes.get("value") and changes["value"].get("messages"):
                message = changes["value"]["messages"][0]
                if message["type"] == "text":
                    return True

    return False


@app.post("/api/query")
async def query(request: Request, status=200):

    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        req_id = generate()
        req_data = {
            "req_id": req_id,
            "req_timestamp": now,
        }
        query_data = await request.body()
        query_data_decoded = query_data.decode('utf-8')
        data = json.loads(query_data_decoded)

        if not process_whatsapp_msg(data):
            raise HTTPException(
                status_code=404, detail="not a whatsapp message")

        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        text = message["text"]["body"]
        sanitized_text = process_user_question_with_emojis(text)
        if sanitized_text == "" or sanitized_text == None or sanitized_text.strip() == "":
            raise HTTPException(
                status_code=404, detail="empty question")

        message["text"]["body"] = sanitized_text

        custom_obj = {
            "metadata": data["entry"][0]["changes"][0]["value"]["metadata"],
            "message": message,
            "contact_info": data["entry"][0]["changes"][0]["value"]["contacts"][0],
            "entry_id": data["entry"][0]["id"]
        }

        data = {
            "req_metrics": req_data,
            "webhook_msg": custom_obj
        }
        logger.info(
            f"Server hit - Question={json.dumps(message)} [Request ID: {req_id}]")

        channel.basic_publish(
            exchange="",
            routing_key=constants.ASK_QUESTION_QUEUE_NAME,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except HTTPException:
        pass
    except Exception as err:
        error_message = traceback.format_exc()
        err = f'Error in /api/query: {str(err)} Stack: {error_message} [Req: {req_data}]'
        logger.error(err)

    return "success"


@app.get("/api/logs", response_model=List[dict])
def get_logs(last_id: int = Query(0, description="Last fetched log ID")):
    # Adjust the range as needed
    query = {"id": {"$gt": last_id, "$lte": last_id + 5000}}
    logs = logs_collection.find(query)
    logs_list = [
        {**log, "_id": str(log["_id"])} for log in list(logs)
    ]

    return logs_list


if __name__ == "__main__":
    # Define the uvicorn command you want to run. Replace 'app:app' with your actual ASGI application module and instance.
    uvicorn_command = [
        "uvicorn",
        "api-server.main:app",  # Replace with your ASGI application module and instance
        "--host", "0.0.0.0",  # Host address
        "--port", "8000",       # Port number
    ]

    try:
        logger.info("API server starting..")
        subprocess.run(uvicorn_command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running uvicorn: {e}")
    except Exception as err:
        logger.error(f"Server: {err}")
    finally:
        logger.info("API server shutdown...")
        # Close the channel
        if channel is not None:
            channel.close()

        # Close the connection
        if connection is not None:
            connection.close()

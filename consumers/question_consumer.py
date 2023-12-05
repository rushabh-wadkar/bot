import pika
import json
import sys
import os
import traceback
from datetime import datetime
import constants
from rmqLogger import RMQLogger
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate
import time
import requests
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import pymongo

logger = RMQLogger()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = constants.MODEL_SECRET_FILEPATH

logger.info("Configuring DB")
conn = pymongo.MongoClient(constants.DB_HOST, port=constants.DB_PORT, username=constants.DB_USERNAME,
                           password=constants.DB_PASSWORD, authSource=constants.DB_DATABASE_NAME, authMechanism='SCRAM-SHA-256')
# conn = pymongo.MongoClient("mongodb://dev:admindev@192.168.0.141:27017/aidb")
db = conn[constants.DB_DATABASE_NAME]
chats_collection = db[constants.DB_TABLE_CHATS]
# chats_collection.create_index([("chat_from", 1)], unique=True)
logger.info("Db configuration successfull..")

credentials = pika.PlainCredentials(
    constants.RMQ_USERNAME, constants.RMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(constants.RMQ_HOST, credentials=credentials, heartbeat=0))
channel = connection.channel()

# Channel configuration for question queue
channel.queue_declare(queue=constants.ASK_QUESTION_QUEUE_NAME, durable=True)
channel.queue_declare(queue=constants.MODEL_CONFIG_QUEUE, durable=True)

# Channel configuration for injest queue
channel.exchange_declare(
    exchange=constants.MODEL_CONFIG_EXCHANGE, exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=constants.MODEL_CONFIG_EXCHANGE, queue=queue_name)


###### LOAD DATA #############
embeddings = VertexAIEmbeddings()
db = FAISS.load_local(folder_path=constants.MODEL_DB_SAVE_PATH,
                      embeddings=embeddings, index_name=constants.MODEL_DB_INDEX_NAME)
retriever = db.as_retriever(search_type=constants.MODEL_SEARCH_TYPE, search_kwargs={
                            "k": constants.MODEL_SEARCH_K})

llm = VertexAI(
    model_name=constants.MODEL_NAME,
    max_output_tokens=constants.MODEL_MAX_OUTPUT_TOKEN,
    temperature=constants.MODEL_TEMPERATURE,
    verbose=constants.MODEL_VERBOSE
)

# template = """You are a female chatbot assistant for the MOTN (also known as Mother of Nation) festival. Your purpose is to provide warm and gentle responses strictly related to the MOTN festival. Please refrain from answering anything not related to the festival or its context. Use language detection to ensure you respond in the same language as the user's question. If the question is in Arabic, respond in Arabic; Otherwise, respond in English. If you don't know the answer, state that you don't know and do not provide unrelated information.
# Always elaborate on your answer in two or three sentences based on the context if you find any relevant documents.

# Context: {context}

# Question: {question}
# # Helpful Answer:"""

# PROMPT = PromptTemplate(template=template, input_variables=[
#                         'context', 'question'])

template = """Act as a female assistant for the MOTN (also known as Mother of Nation) festival who is having a friendly conversation. You are talkative and provides lots of specific details from its context.
Strictly Answer based on the below context only in the most humble, gentle, responsible and empathetic way. Please refrain from answering anything not related to the festival or its context. Use language detection to ensure you respond in the same language as the user's question. If the question is in Arabic, respond in Arabic; Otherwise, respond in English. If you don't know the answer, state that you don't know and do not provide unrelated information.
Please reply appropriately if it's not a question. Also when asked about food/event or any options request, please do explain each thing elaborately with summarized description properly.

Context: {context}

Current conversation:
{chat_history}
Human: {question}
AI Assistant:"""

PROMPT = PromptTemplate(template=template, input_variables=[
                        'context', 'question', 'chat_history'])

memory = ConversationBufferMemory(
    memory_key="chat_history", ai_prefix="AI Assistant", return_messages=True)
# chat = RetrievalQA.from_chain_type(
#     llm=llm, chain_type="stuff", retriever=retriever, memory=memory, verbose=constants.MODEL_VERBOSE, chain_type_kwargs={
#         "prompt": PROMPT,
#         "verbose": constants.MODEL_VERBOSE
#     },)

chat = ConversationalRetrievalChain.from_llm(
    llm, retriever, memory=memory, combine_docs_chain_kwargs={"prompt": PROMPT}, verbose=True)

updated_db_index = None
# db2 = FAISS.from_texts(
#     ["Time required for the MARSHALL ride is 10mins."], embeddings)
# db.merge_from(db2)
# updated_db_index = db2.index_to_docstore_id[0]
logger.info("Chat object ready to roll..")


def handle_model_injest_msg_callback(ch, method, properties, body):
    global updated_db_index

    request = json.loads(body)
    value = request["value"]
    string = f"Time required for the MARSHALL ride is {value}."

    db.delete([updated_db_index])
    db2 = FAISS.from_texts([string], embeddings)
    db.merge_from(db2)
    updated_db_index = db2.index_to_docstore_id[0]
    print(
        f"Awesome, Got msg in model injest queue: string: {string}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_model_injest_channel(channel):
    channel.basic_consume(
        queue=queue_name, on_message_callback=handle_model_injest_msg_callback
    )


def fetch_previous_questions(chat_from):
    try:
        # Define the filter, projection, sort, and limit for the query
        filter_query = {"chat_from": chat_from}
        projection = {"_id": 0, "chat_question": 1, "chat_answer": 1}
        sort_query = [("chat_timestamp", -1)]
        limit = 10

        # Execute the query
        cursor = chats_collection.find(
            filter_query, projection).sort(sort_query).limit(limit)

        # Iterate over the cursor and print each document
        lst = [document for document in cursor]
        if lst is not None and len(lst) > 0:
            lst.reverse()
        return lst
    except Exception as err:
        error_message = traceback.format_exc()
        err = f'Error in fetch_previous_questions: {str(err)} Stack: {error_message}'
        logger.error(err)
    return []


def handle_question_callback(ch, method, properties, body):
    try:
        fn_start_time = time.time()
        message = json.loads(body)

        req_id = message["req_metrics"]["req_id"]
        req_time = message["req_metrics"]["req_timestamp"]
        model_req_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        # Fetch query text from object
        question = message["webhook_msg"]["message"]["text"]["body"]
        phone_number_id = message["webhook_msg"]["metadata"]["phone_number_id"]
        from_number = message["webhook_msg"]["message"]["from"]
        chat_id = message["webhook_msg"]["message"]["id"]
        chat_timestamp = datetime.fromtimestamp(
            float(message["webhook_msg"]["message"]["timestamp"]))
        chat_profile = message["webhook_msg"]["contact_info"]
        chat_entry_id = message["webhook_msg"]["entry_id"]

        chat.memory.clear()
        chat.memory.chat_memory.clear()

        if constants.FETCH_PREVIOUS_QUESTIONS:
            q_list = fetch_previous_questions(from_number)

            for item in q_list:
                chat.memory.chat_memory.add_user_message(
                    message=item["chat_question"])
                chat.memory.chat_memory.add_ai_message(
                    message=item["chat_answer"])

        result = chat({"question": question}, return_only_outputs=True)
        response = result["answer"]
        if response == None or response == "" or len(response) == 0:
            response = "I'm sorry, I couldn't generate a response at the moment. Please feel free to ask something else or try again later."
        elif response.startswith("Answer:"):
            response = response[len("Answer:"):]

        response = response.strip()
        # response = response.replace("\n", ".")
        # response = response.replace("\t", " ")

        model_response_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        total_processing_time = time.time() - fn_start_time
        # print(f"[Question]: {question} ------> {response} ### [ Time: {total_processing_time}]")

        url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages?access_token={constants.WHATSAPP_TOKEN}"
        payload = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "text": {"body": f"{response}"}
        }
        headers = {"Content-Type": "application/json"}

        http_response = requests.post(url, json=payload, headers=headers)

        chats_collection.insert_one({
            "request_id": req_id,
            "request_timestamp_api": req_time,
            "request_timestamp_model": model_req_time,
            "chat_question": question,
            "chat_answer": response,
            "chat_from": from_number,
            "chat_id": chat_id,
            "chat_timestamp": chat_timestamp,
            "chat_profile": chat_profile,
            "chat_entry_id": chat_entry_id,
            "response_timestamp_model": model_response_time,
            "model_processing_time": total_processing_time
        })

        ch.basic_ack(delivery_tag=method.delivery_tag)
        http_response.raise_for_status()
    except Exception as err:
        error_message = traceback.format_exc()
        err = f'Error in processing question: {str(err)} Stack: {error_message} [Req: {message}]'
        logger.error(err)


def consume_question_channel(channel):
    channel.basic_consume(
        queue=constants.ASK_QUESTION_QUEUE_NAME, on_message_callback=handle_question_callback
    )


def run():
    logger.info("Started consumer")
    consume_question_channel(channel)

    consume_model_injest_channel(channel)

    logger.info("Waiting for messages. To exit press CTRL+C")
    print("Starting...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        run()
    except Exception as err:
        # Close the channel
        channel.close()

        # Close the connection
        connection.close()

        # Close DB
        conn.close()

        error_message = traceback.format_exc()
        err = f'Error in consumer service: {str(err)} Stack: {error_message}'
        print(err)
        logger.error(err)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

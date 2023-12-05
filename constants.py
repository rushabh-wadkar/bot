import os


# RMQ Exchanges & CONFIG
RMQ_HOST = os.environ.get('RMQ_HOST', 'localhost')
RMQ_USERNAME = os.environ.get('RMQ_USERNAME', 'root')
RMQ_PASSWORD = os.environ.get('RMQ_PASSWORD', 'rootuser@9907')
MODEL_CONFIG_EXCHANGE = "MODEL_CONFIG_EXCHANGE"

# RMQ Queues
ASK_QUESTION_QUEUE_NAME = 'QUESTION_QUEUE'
INSERT_INTO_DB_QUEUE_NAME = 'DB_UPSERT_QUEUE'
LOGS_QUEUE_NAME = 'LOGS_INSERT_QUEUE'
MODEL_CONFIG_QUEUE = 'MODEL_CONFIG_QUEUE'


# CREDENTIALS
DB_HOST = os.environ.get('DB_HOST', '192.168.0.141')
DB_PORT = int(os.environ.get('DB_PORT', 27017))
DB_USERNAME = os.environ.get('DB_USERNAME', 'dev')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admindev')
DB_DATABASE_NAME = os.environ.get('DB_DATABASE_NAME', 'aidb')

# DB TABLE NAME
DB_TABLE_LOGS = 'logs'
DB_TABLE_CHATS = 'chats'

# Model
MODEL_SECRET_FILEPATH = './consumers/secrets/aichatbot-406213-093638009277.json'
MODEL_BATCH_CHUNK_SIZE = 1500
MODEL_CHUNK_OVERLAP = 100
MODEL_DATA_PATH = './consumers/data'
MODEL_DB_SAVE_PATH = './consumers/db'
MODEL_DB_INDEX_NAME = 'data_injest'
MODEL_SEARCH_TYPE = 'similarity'
MODEL_SEARCH_K = 5

MODEL_NAME = 'text-bison@001'
MODEL_MAX_OUTPUT_TOKEN = 800
# MODEL_TOP_P = 0.9
MODEL_TEMPERATURE = 0.3
MODEL_VERBOSE = False


# Whatsapp Setup
VERIFY_TOKEN = "k4YGEk6D6q9S6R832zqNDPKCsmK2Z4rwdcMtWdDZUf6Gpu8WmU"
WHATSAPP_TOKEN = "EAAKUbxDh3QIBOZChw1xzar25qIWS7goisxKKP8qL5TriCdgcPCy5i22WTlTZCLIocUFzgBSyb0orohhsbF4ZCeusvLTNuNPUVcaCDyAgW5QgZAbe1vEsJZBtAr910BYcd3c2ER0uKkKXHNRXw2lkb3ZBM9T4fT1N085fxwVN2UZB0BruX7gyeURkqEHYQ3Sbb2zqXqgSUuR8ZA6H1dZApLqKQgBAwoSokXqnFGcWqjaoZD"


# CONSUMER CONFIG
FETCH_PREVIOUS_QUESTIONS = True

SHOW_LOGS = os.environ.get('SHOW_LOGS', True)

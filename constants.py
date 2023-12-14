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
MODEL_BATCH_CHUNK_SIZE = 300
MODEL_CHUNK_OVERLAP = 50
MODEL_DATA_PATH = './consumers/data/textfiles/'
MODEL_DB_SAVE_PATH = './consumers/db'
MODEL_DB_INDEX_NAME = 'data_injest'
MODEL_SEARCH_TYPE = 'similarity'
MODEL_SEARCH_K = 3

MODEL_NAME = "text-bison@002"
MODEL_MAX_OUTPUT_TOKEN = 500
# MODEL_TOP_P = 0.9
MODEL_TEMPERATURE = 0.1
MODEL_VERBOSE = False


# Whatsapp Setup
VERIFY_TOKEN = "k4YGEk6D6q9S6R832zqNDPKCsmK2Z4rwdcMtWdDZUf6Gpu8WmU"
WHATSAPP_TOKEN = "EAAp23ZBtc9NsBOZBJnD2rSSryZCNvoCMuHejpA96nYwcafOaxEkLdNFvSU9dJTbJp7kjRJAjeIu3kOBH6f0ZAc9RhS3ZA2BGZAvyLHm8UkGS2m2vVBxPt2dz06bmYaaVfNudXaPsQZBNfMrdNrggIuy50fgSmQNGxdZCoMPTXXNhG5GDsXAkIF9Va2a5uXV6nnpfrDrZBgUgZChK77EvL5eevCqiMKnGnFZCaoOxPO613QZD"


# CONSUMER CONFIG
FETCH_PREVIOUS_QUESTIONS = True

SHOW_LOGS = os.environ.get('SHOW_LOGS', False)

PREDEFINED_ANSWERS = {
    "hi": [
        "Hello! 🌟 Welcome to our chat! I'm here to assist you with anything you need to about MOTN festival, it's a month-long extravaganza of entertainment and joy 🌟",
        "Hello there! 👋 It's such a pleasure to have you here. If there's anything on your mind about MOTN festival, feel free to let me know.",
        "Hey! 😊 I'm so glad you dropped by! If there's anything I can do for you, just say the word. Oh, and have you heard the buzz about the MOTN festival? Sounds like a fantastic event you wouldn't want to miss! 🌟",
        "Hello! 👋 It's wonderful to see you here! How can I assist you today? Also, did you know about the MOTN festival? It's creating quite a stir with its 24 days of exciting festivities and New Year's Eve celebration! 🌟",
        "Hi there! 👋 I hope your day is going well! If there's anything you'd like help with, feel free to ask.",
        "Hello! 😊 I'm here and ready to assist you with anything you need.",
        "Hey! 🌟 Welcome to our chat space! If there's anything I can do for you, just let me know. Oh, and speaking of exciting things, have you considered attending the MOTN festival? It's the talk of the town! 🌟",
        "Hello there! 😊 It's a pleasure to have you in the conversation. If you have any questions or need assistance about MOTN festival, feel free to ask.",
        "Hi! 👋 I'm here and ready to help you out. If there's anything specific on your mind, let me know. Also, have you heard about the MOTN festival? It's the highlight of the season with 24 days of festivities! 🌟",
        "Hello! 👋 So glad you're here! If there's anything you'd like assistance with, feel free to ask. And by the way, have you considered joining the excitement at the MOTN festival? It's going to be a month-long celebration! 🌟"
    ],
    "hello": [
        "Hello! 🌟 Welcome to our chat! I'm here to assist you with anything you need to about MOTN festival, it's a month-long extravaganza of entertainment and joy 🌟",
        "Hello there! 👋 It's such a pleasure to have you here. If there's anything on your mind about MOTN festival, feel free to let me know.",
        "Hey! 😊 I'm so glad you dropped by! If there's anything I can do for you, just say the word. Oh, and have you heard the buzz about the MOTN festival? Sounds like a fantastic event you wouldn't want to miss! 🌟",
        "Hello! 👋 It's wonderful to see you here! How can I assist you today? Also, did you know about the MOTN festival? It's creating quite a stir with its 24 days of exciting festivities and New Year's Eve celebration! 🌟",
        "Hi there! 👋 I hope your day is going well! If there's anything you'd like help with, feel free to ask.",
        "Hello! 😊 I'm here and ready to assist you with anything you need.",
        "Hey! 🌟 Welcome to our chat space! If there's anything I can do for you, just let me know. Oh, and speaking of exciting things, have you considered attending the MOTN festival? It's the talk of the town! 🌟",
        "Hello there! 😊 It's a pleasure to have you in the conversation. If you have any questions or need assistance about MOTN festival, feel free to ask.",
        "Hi! 👋 I'm here and ready to help you out. If there's anything specific on your mind, let me know. Also, have you heard about the MOTN festival? It's the highlight of the season with 24 days of festivities! 🌟",
        "Hello! 👋 So glad you're here! If there's anything you'd like assistance with, feel free to ask. And by the way, have you considered joining the excitement at the MOTN festival? It's going to be a month-long celebration! 🌟"
    ],
    "hey": [
        "Hello! 🌟 Welcome to our chat! I'm here to assist you with anything you need to about MOTN festival, it's a month-long extravaganza of entertainment and joy 🌟",
        "Hello there! 👋 It's such a pleasure to have you here. If there's anything on your mind about MOTN festival, feel free to let me know.",
        "Hey! 😊 I'm so glad you dropped by! If there's anything I can do for you, just say the word. Oh, and have you heard the buzz about the MOTN festival? Sounds like a fantastic event you wouldn't want to miss! 🌟",
        "Hello! 👋 It's wonderful to see you here! How can I assist you today? Also, did you know about the MOTN festival? It's creating quite a stir with its 24 days of exciting festivities and New Year's Eve celebration! 🌟",
        "Hi there! 👋 I hope your day is going well! If there's anything you'd like help with, feel free to ask.",
        "Hello! 😊 I'm here and ready to assist you with anything you need.",
        "Hey! 🌟 Welcome to our chat space! If there's anything I can do for you, just let me know. Oh, and speaking of exciting things, have you considered attending the MOTN festival? It's the talk of the town! 🌟",
        "Hello there! 😊 It's a pleasure to have you in the conversation. If you have any questions or need assistance about MOTN festival, feel free to ask.",
        "Hi! 👋 I'm here and ready to help you out. If there's anything specific on your mind, let me know. Also, have you heard about the MOTN festival? It's the highlight of the season with 24 days of festivities! 🌟",
        "Hello! 👋 So glad you're here! If there's anything you'd like assistance with, feel free to ask. And by the way, have you considered joining the excitement at the MOTN festival? It's going to be a month-long celebration! 🌟"
    ],
    "sorry": [
        "No need to apologize at all! 😊 Life happens.",
        "No worries! 😌 If there's anything on your mind, feel free to share.",
        "It's all good! 😄 No need to say sorry.",
        "No problem at all! 😊 Your presence here is what matters.",
        "No need to apologize! 😎 If there's anything you'd like to know or discuss, feel free.",
        "No apology necessary! 😊 We're here for you.",
        "No worries at all! 😌 Life happens, and we're here to make things brighter.",
        "It's absolutely fine! 😄 No need to apologize.",
        "No problem at all! 😊 Your presence is what matters most.",
        "No need to apologize! 😎 If there's anything you'd like to talk about or explore, feel free to let me know."
    ],
    "ok": [
        "Alright! 😊 If you have any questions or need information, feel free to ask.",
        "Got it! 👍 If there's anything specific on your mind, let me know.",
        "Okay, sounds good! 😄 If there's anything else you'd like to know, feel free to ask.",
        "Alright, no problem! 😌 If you change your mind or have more questions, I'm here.",
        "Okay, got it! 😊 If there's anything specific you're interested in, feel free to mention it.",
        "Okay, no worries! 👌 If there's anything else you'd like to discuss, feel free to let me know.",
        "Gotcha! 👍 If there's anything specific you're looking for, just let me know.",
        "Okay, understood! 😄 If you have any more questions or need assistance, feel free to ask.",
        "Alright then! 😊 If there's anything else on your mind, feel free to share.",
        "Okay, no problem! 😌 If there's anything specific you're curious about, feel free to let me know."
    ],
    "fine": [
        "Alright! 😊 If you have any questions or need information, feel free to ask.",
        "Got it! 👍 If there's anything specific on your mind, let me know.",
        "Okay, sounds good! 😄 If there's anything else you'd like to know, feel free to ask.",
        "Alright, no problem! 😌 If you change your mind or have more questions, I'm here.",
        "Okay, got it! 😊 If there's anything specific you're interested in, feel free to mention it.",
        "Okay, no worries! 👌 If there's anything else you'd like to discuss, feel free to let me know.",
        "Gotcha! 👍 If there's anything specific you're looking for, just let me know.",
        "Okay, understood! 😄 If you have any more questions or need assistance, feel free to ask.",
        "Alright then! 😊 If there's anything else on your mind, feel free to share.",
        "Okay, no problem! 😌 If there's anything specific you're curious about, feel free to let me know."
    ],
    "welcome": [
        "Thank you! 😊 It's my pleasure to assist.",
        "Thank you for your kind words! 🌟 If you have any more questions or need information, feel free to ask.",
        "You're welcome! 😄 If there's anything else I can help you with, just let me know.",
        "No problem at all! 😎 Your gratitude is appreciated. If there's anything else on your mind, feel free to ask.",
        "You're welcome! 👍 If there's anything specific you're looking for, feel free to mention it.",
        "It's my pleasure! 😊 If you have more questions or need assistance in the future, don't hesitate to ask.",
        "No worries at all! 😌 If there's anything else you'd like to know or discuss, feel free to let me know.",
        "You're welcome! 😄 If there's anything specific on your mind, feel free to share.",
        "It's no trouble at all! 😊 If you ever need assistance in the future, I'm here.",
        "Anytime! 👌 If there's anything else you'd like to discuss or explore, feel free to let me know."
    ],
    "bye": [
        "Goodbye! 😊 If you ever have more questions or just want to chat, feel free to come back. Have a fantastic day!",
        "Bye! 👋 It was great chatting with you. If you ever need assistance in the future, don't hesitate to reach out. Take care!",
        "Farewell! 😄 If there's anything else you'd like to know later on, don't be a stranger. Wishing you a wonderful day ahead!",
        "Goodbye! 😌 It was a pleasure assisting you. If you ever want to talk or have more questions, remember I'm here. Take care and enjoy your day!",
        "See you! 😄 If there's anything else on your mind in the future, feel free to drop by. Have a fantastic time, and goodbye for now!"
    ]
}

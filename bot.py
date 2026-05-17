from flask import Flask
from threading import Thread
import asyncio
from telegram import Bot

app = Flask('')

@app.route('/')
def home():
    return "Bot actif"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

TELEGRAM_TOKEN = "8962293821:AAH-TmXsuQJPmwNpK2HcW29N7voNjVHaJAA"
CHAT_ID = "7729357640"

BOT = Bot(token=TELEGRAM_TOKEN)

async def envoyer():
    await BOT.send_message(
        chat_id=CHAT_ID,
        text="🚗 TEST AUTOLINK BOT OK"
    )

asyncio.run(envoyer())

print("Message envoyé")

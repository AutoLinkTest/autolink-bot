from flask import Flask
from threading import Thread

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

import time
import requests
import feedparser
from bs4 import BeautifulSoup
from telegram import Bot

# =========================
# CONFIG
# =========================

TELEGRAM_TOKEN = "8962293821:AAH-TmXsuQJPmwNpK2HcW29N7voNjVHaJAA"
CHAT_ID = "7729357640"

BOT = Bot(token=TELEGRAM_TOKEN)

PRIX_MAX = 1000

MOTS_INTERDITS = [
    "pour pièces",
    "pour piece",
    "épave",
    "moteur hs",
    "hs",
    "casse"
]

URL_RSS = "https://www.leboncoin.fr/recherche?category=2&text=renault+peugeot+citroen+dacia&price=min-1000"

annonces_vues = set()

# =========================
# TELEGRAM
# =========================

def envoyer_message(message):
    try:
        BOT.send_message(chat_id=CHAT_ID, text=message)
        print("Message envoyé")
    except Exception as e:
        print(e)

# =========================
# FILTRES
# =========================

def annonce_valide(titre):
    titre_lower = titre.lower()

    for mot in MOTS_INTERDITS:
        if mot in titre_lower:
            return False

    return True

# =========================
# SCRAPER
# =========================

def verifier_annonces():

    print("Scan en cours...")

    feed = feedparser.parse(URL_RSS)

    for entry in feed.entries:

        titre = entry.title
        lien = entry.link

        if lien in annonces_vues:
            continue

        annonces_vues.add(lien)

        if not annonce_valide(titre):
            continue

        message = f"""
🚗 Nouvelle annonce

{titre}

🔗 {lien}
"""

        envoyer_message(message)

# =========================
# MAIN
# =========================

envoyer_message("🤖 AutoLink Bot démarré")

while True:

    try:
        verifier_annonces()
    except Exception as e:
        print(e)

    time.sleep(900)

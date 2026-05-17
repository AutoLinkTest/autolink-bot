from flask import Flask
from threading import Thread
import asyncio
import time
import feedparser
from telegram import Bot

# =========================
# FLASK SERVER
# =========================

app = Flask('')

@app.route('/')
def home():
    return "AutoLink Bot actif"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# =========================
# CONFIG
# =========================

TELEGRAM_TOKEN = "TON_TOKEN_ICI"
CHAT_ID = "7729357640"

BOT = Bot(token=TELEGRAM_TOKEN)

# =========================
# RECHERCHE LEBONCOIN
# =========================

URL_RSS = "https://www.leboncoin.fr/recherche?category=2&text=renault+peugeot+citroen+dacia&price=min-1000"

# =========================
# MOTS INTERDITS
# =========================

MOTS_INTERDITS = [
    "pour pièces",
    "pour piece",
    "épave",
    "moteur hs",
    "hs",
    "casse"
]

annonces_vues = set()

# =========================
# ENVOI TELEGRAM
# =========================

async def envoyer_message_async(message):
    await BOT.send_message(
        chat_id=CHAT_ID,
        text=message
    )

def envoyer_message(message):

    try:
        asyncio.run(envoyer_message_async(message))
        print("✅ Message envoyé")

    except Exception as e:
        print(e)

# =========================
# FILTRE ANNONCES
# =========================

def annonce_valide(titre):

    titre = titre.lower()

    for mot in MOTS_INTERDITS:

        if mot in titre:
            return False

    return True

# =========================
# VERIFICATION ANNONCES
# =========================

def verifier_annonces():

    print("🔍 Scan en cours...")

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
🚗 Nouvelle annonce AutoLink

📌 {titre}

🔗 {lien}
"""

        envoyer_message(message)

# =========================
# DEMARRAGE
# =========================

envoyer_message("🤖 AutoLink Bot démarré")

while True:

    try:
        verifier_annonces()

    except Exception as e:
        print(e)

    # scan toutes les 15 minutes
    time.sleep(900)

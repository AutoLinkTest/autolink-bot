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

TELEGRAM_TOKEN = "8962293821:AAH-TmXsuQJPmwNpK2HcW29N7voNjVHaJAA"
CHAT_ID = "7729357640"

BOT = Bot(token=TELEGRAM_TOKEN)

# =========================
# RECHERCHE
# =========================

URL_RSS = "https://www.leboncoin.fr/recherche?category=2&text=renault+peugeot+citroen+dacia&price=min-1000"

# =========================
# FILTRES
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
dernier_heartbeat = ""

# =========================
# TELEGRAM
# =========================

async def envoyer_message_async(message):

    await BOT.send_message(
        chat_id=CHAT_ID,
        text=message
    )

def envoyer_message(message):

    try:

        asyncio.run(
            envoyer_message_async(message)
        )

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
# SCAN ANNONCES
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
# HEARTBEAT
# =========================

def verifier_heartbeat():

    global dernier_heartbeat

    heure = time.strftime("%H:%M")

    if heure == "09:00" and dernier_heartbeat != heure:

        envoyer_message("✅ AutoLink Bot toujours actif")

        dernier_heartbeat = heure

# =========================
# DEMARRAGE
# =========================

envoyer_message("🤖 AutoLink Bot démarré")

# =========================
# BOUCLE PRINCIPALE
# =========================

while True:

    try:

        verifier_annonces()
        verifier_heartbeat()

    except Exception as e:

        print(e)

    # Scan toutes les 15 minutes
    time.sleep(900)

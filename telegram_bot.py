# ==========================================================
# TELEGRAM BOT
# V6.1
# ==========================================================

import requests

from config import (
    TOKEN,
    CHAT_ID
)


# ==========================================================
# INVIO MESSAGGIO
# ==========================================================

def send_message(message):

    if not message.strip():

        print("Nessun messaggio da inviare.")

        return

    response = requests.post(

        f"https://api.telegram.org/bot{TOKEN}/sendMessage",

        json={

            "chat_id": CHAT_ID,

            "text": message

        },

        timeout=20

    )

    print(response.json())


# ==========================================================
# COSTRUZIONE MESSAGGIO
# ==========================================================

def build_message(

    signals,

    pre_long,

    watchlist

):

    message = ""

    # ======================================================
    # LONG
    # ======================================================

    if signals:

        message += "🟢 LONG SETUP\n\n"

        for s in signals:

            message += (

                f"🪙 {s['symbol']}\n"

                f"Trend: {s['trend_score']}/3\n"

                f"Entry: {s['entry']:.2f}\n"

                f"Stop: {s['stop']:.2f}\n"

                f"TP1: {s['tp1']:.2f}\n"

                f"TP2: {s['tp2']:.2f}\n"

                f"RR: {s['rr']:.2f}\n"

                f"Rischio: {s.get('risk_percent', 0):.2f}%\n"

                f"RVOL: {s['rvol']:.2f}\n\n"

            )

    # ======================================================
    # PRE LONG
    # ======================================================

    if pre_long:

        message += "🟠 PRE-LONG\n\n"

        for p in pre_long:

            message += (

                f"🪙 {p['symbol']}\n"

                f"Score: {p['score']:.1f}\n"

                f"Trend: {p['trend_score']}/3\n"

                f"Distanza: {p['distance']:.2f}%\n"

                f"RVOL: {p['rvol']:.2f}\n\n"

            )

    # ======================================================
    # WATCHLIST
    # ======================================================

    if watchlist:

        message += "🟡 WATCHLIST\n\n"

        for w in watchlist:

            support = "-"

            if w["support"] is not None:

                support = f"{w['support']:.2f}"

            message += (

                f"🪙 {w['symbol']}\n"

                f"Prezzo: {w['close']:.2f}\n"

                f"Supporto: {support}\n"

                f"Resistenza: {w['resistance']:.2f}\n"

                f"Distanza: {w['distance']:.2f}%\n"

                f"Trend: {w['trend_score']}/3\n"

                f"Score: {w['score']:.1f}\n"

                f"RVOL: {w['rvol']:.2f}\n\n"

            )

    if message == "":

        message = "Nessun setup trovato."

    return message

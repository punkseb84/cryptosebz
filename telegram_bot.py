import requests

from config import (
    TOKEN,
    CHAT_ID
)


# ==========================================================
# LONG
# ==========================================================

def build_long_section(signals):

    if not signals:
        return ""

    text = "🟢 LONG SETUP\n\n"

    for s in signals:

        text += (
            f"{s['symbol']}\n"
            f"Entry: {s['entry']:.2f}\n"
            f"Stop: {s['stop']:.2f}\n"
            f"TP1: {s['tp1']:.2f}\n"
            f"TP2: {s['tp2']:.2f}\n"
            f"RR: {s['rr']:.2f}\n"
            f"Trend: {s['trend_score']}/3\n"
            f"RVOL: {s['rvol']:.2f}\n\n"
            f"Supporto: {s['stop']:.2f}\n"
        )

    return text


# ==========================================================
# PRE LONG
# ==========================================================

def build_prelong_section(pre_long):

    if not pre_long:
        return ""

    text = "🟠 PRE-LONG\n\n"

    for p in pre_long:

        text += (
            f"{p['symbol']}\n"
            f"Score: {p['score']:.1f}\n"
            f"Trend: {p['trend_score']}/3\n"
            f"Distanza: {p['distance']:.2f}%\n"
            f"RVOL: {p['rvol']:.2f}\n\n"
        )

    return text


# ==========================================================
# WATCHLIST
# ==========================================================

def build_watchlist_section(watchlist):

    if not watchlist:
        return ""

    text = "🟡 WATCHLIST\n\n"

    for w in watchlist:

        text += (
            f"{w['symbol']}\n"
            f"Prezzo: {w['close']:.2f}\n"
            f"Supporto: {w['support']:.2f}\n"
            f"Resistenza: {w['resistance']:.2f}\n"
            f"Distanza: {w['distance']:.2f}%\n"
            f"Trend: {w['trend_score']}/3\n"
            f"Score: {w['score']:.1f}\n"
            f"RVOL: {w['rvol']:.2f}\n\n"
        )

    return text


# ==========================================================
# BUILD MESSAGE
# ==========================================================

def build_message(

    signals,

    pre_long,

    watchlist

):

    message = ""

    message += build_long_section(signals)

    message += build_prelong_section(pre_long)

    message += build_watchlist_section(watchlist)

    return message


# ==========================================================
# SEND TELEGRAM
# ==========================================================

def send_message(message):

    if not message:

        print("Nessun setup trovato")

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

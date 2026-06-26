# ==========================================================
# TELEGRAM BOT
# ==========================================================

import requests

from config import CHAT_ID, TOKEN


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
            "text": message,
        },
        timeout=20,
    )

    print(response.json())


# ==========================================================
# COSTRUZIONE MESSAGGIO
# ==========================================================

def build_message(signal):
    emoji = "🟢" if signal["direction"] == "LONG" else "🔴"
    level_reason = "Supporto vicino o breakout confermato"
    ema_reason = "EMA 20 > EMA 50 su 5m"
    macd_reason = "MACD positivo o in miglioramento"

    if signal["direction"] == "SHORT":
        level_reason = "Resistenza vicina o breakdown confermato"
        ema_reason = "EMA 20 < EMA 50 su 5m"
        macd_reason = "MACD negativo o in peggioramento"

    return (
        f"{emoji} {signal['direction']} {signal['symbol']}/USD\n"
        f"Entry: {signal['entry']:.2f}\n"
        f"Stop Loss: {signal['stop']:.2f}\n"
        f"Target 1: {signal['tp1']:.2f}\n"
        f"Target 2: {signal['tp2']:.2f}\n"
        "Timeframe: 5m\n"
        "Trend: confermato su 15m e 1h\n"
        "Motivi:\n"
        "- Trend 1h favorevole\n"
        "- Conferma 15m favorevole\n"
        f"- {ema_reason}\n"
        "- RSI in zona operativa\n"
        f"- {macd_reason}\n"
        "- Volume sufficiente\n"
        f"- {level_reason}"
    )

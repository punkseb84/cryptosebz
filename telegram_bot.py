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

def signal_reasons(signal):
    level_reason = "Supporto vicino o breakout confermato"
    ema_reason = "EMA 20 > EMA 50 su 5m"
    macd_reason = "MACD positivo o in miglioramento"

    if signal["direction"] == "SHORT":
        level_reason = "Resistenza vicina o breakdown confermato"
        ema_reason = "EMA 20 < EMA 50 su 5m"
        macd_reason = "MACD negativo o in peggioramento"

    return [
        "Trend 1h favorevole",
        "Conferma 15m favorevole",
        ema_reason,
        "RSI in zona operativa",
        macd_reason,
        "Volume sufficiente",
        level_reason,
    ]


def build_message(signal):
    emoji = "🟢" if signal["direction"] == "LONG" else "🔴"
    reasons = signal_reasons(signal)

    return (
        f"{emoji} {signal['direction']} {signal['symbol']}/USD\n"
        f"Entry: {signal['entry']:.2f}\n"
        f"Stop Loss: {signal['stop']:.2f}\n"
        f"Target 1: {signal['tp1']:.2f}\n"
        f"Target 2: {signal['tp2']:.2f}\n"
        "Timeframe: 5m\n"
        "Trend: confermato su 15m e 1h\n"
        "Motivi:\n"
        + "\n".join(f"- {reason}" for reason in reasons)
    )

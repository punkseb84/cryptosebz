import os
import requests
import pandas as pd
from ta.trend import EMAIndicator

# TELEGRAM

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# KRAKEN OHLC 4H

url = "https://api.kraken.com/0/public/OHLC"

params = {
    "pair": "XBTUSD",
    "interval": 240
}

response = requests.get(url, params=params)

data = response.json()

print(data)

pair_name = list(data["result"].keys())[0]

candles = data["result"][pair_name]

df = pd.DataFrame(
    candles,
    columns=[
        "time",
        "open",
        "high",
        "low",
        "close",
        "vwap",
        "volume",
        "count"
    ]
)

df["close"] = df["close"].astype(float)

# EMA20

df["ema20"] = EMAIndicator(
    close=df["close"],
    window=20
).ema_indicator()

price = df.iloc[-1]["close"]
ema20 = df.iloc[-1]["ema20"]

trend = (
    "RIALZISTA"
    if price > ema20
    else "RIBASSISTA"
)

message = f"""
📊 BTC/USD 4H

Prezzo:
{price:.2f}

EMA20:
{ema20:.2f}

Trend:
{trend}
"""

telegram_url = (
    f"https://api.telegram.org/bot{TOKEN}/sendMessage"
)

response = requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.json())

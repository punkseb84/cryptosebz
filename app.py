import os
import requests
import pandas as pd
from ta.trend import EMAIndicator

# ==========================================
# TELEGRAM
# ==========================================

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ==========================================
# KRAKEN OHLC 4H
# ==========================================

url = "https://api.kraken.com/0/public/OHLC"

params = {
    "pair": "XBTUSD",
    "interval": 240
}

response = requests.get(url, params=params)
data = response.json()

# Trova il nome della coppia restituita da Kraken
pair_name = [
    key for key in data["result"].keys()
    if key != "last"
][0]

candles = data["result"][pair_name]

# ==========================================
# DATAFRAME
# ==========================================

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

# Conversione numerica

df["open"] = df["open"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)
df["close"] = df["close"].astype(float)
df["volume"] = df["volume"].astype(float)

# ==========================================
# EMA20
# ==========================================

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

# ==========================================
# SWING HIGH / SWING LOW
# ==========================================

swing_highs = []
swing_lows = []

for i in range(2, len(df) - 2):

    current_high = df.iloc[i]["high"]

    if (
        current_high > df.iloc[i - 1]["high"]
        and current_high > df.iloc[i - 2]["high"]
        and current_high > df.iloc[i + 1]["high"]
        and current_high > df.iloc[i + 2]["high"]
    ):
        swing_highs.append(current_high)

    current_low = df.iloc[i]["low"]

    if (
        current_low < df.iloc[i - 1]["low"]
        and current_low < df.iloc[i - 2]["low"]
        and current_low < df.iloc[i + 1]["low"]
        and current_low < df.iloc[i + 2]["low"]
    ):
        swing_lows.append(current_low)

# ==========================================
# SUPPORTO E RESISTENZA PIÙ VICINI
# ==========================================

resistances_above = [
    level for level in swing_highs
    if level > price
]

supports_below = [
    level for level in swing_lows
    if level < price
]

resistance = (
    min(resistances_above)
    if len(resistances_above) > 0
    else None
)

support = (
    max(supports_below)
    if len(supports_below) > 0
    else None
)

res_text = (
    f"{resistance:.2f}"
    if resistance is not None
    else "N/D"
)

sup_text = (
    f"{support:.2f}"
    if support is not None
    else "N/D"
)

# ==========================================
# MESSAGGIO TELEGRAM
# ==========================================

message = f"""
📊 BTC/USD 4H

Prezzo:
{price:.2f}

EMA20:
{ema20:.2f}

Trend:
{trend}

Resistenza più vicina:
{res_text}

Supporto più vicino:
{sup_text}
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

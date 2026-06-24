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

print(data)

# Kraken restituisce:
# result -> XXBTZUSD + last

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
# SWING HIGH / LOW
# ==========================================

swing_highs = []
swing_lows = []

for i in range(2, len(df) - 2):

    high = df.iloc[i]["high"]

    if (
        high > df.iloc[i - 1]["high"]
        and high > df.iloc[i - 2]["high"]
        and high > df.iloc[i + 1]["high"]
        and high > df.iloc[i + 2]["high"]
    ):
        swing_highs.append(high)

    low = df.iloc[i]["low"]

    if (
        low < df.iloc[i - 1]["low"]
        and low < df.iloc[i - 2]["low"]
        and low < df.iloc[i + 1]["low"]
        and low < df.iloc[i + 2]["low"]
    ):
        swing_lows.append(low)

# ==========================================
# SUPPORTO E RESISTENZA
# ==========================================

if len(swing_highs) >= 5:
    resistance = max(swing_highs[-5:])
else:
    resistance = max(swing_highs)

if len(swing_lows) >= 5:
    support = min(swing_lows[-5:])
else:
    support = min(swing_lows)

# ==========================================
# TELEGRAM MESSAGE
# ==========================================

message = f"""
📊 BTC/USD 4H

Prezzo:
{price:.2f}

EMA20:
{ema20:.2f}

Trend:
{trend}

Resistenza:
{resistance:.2f}

Supporto:
{support:.2f}
"""

telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.json())

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
# DATI KRAKEN 4H
# ==========================================

url = "https://api.kraken.com/0/public/OHLC"

params = {
    "pair": "XBTUSD",
    "interval": 240
}

response = requests.get(url, params=params)
data = response.json()

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

for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

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
    if resistances_above
    else None
)

support = (
    max(supports_below)
    if supports_below
    else None
)

# ==========================================
# ZONA RESISTENZA
# ==========================================

resistance_zone = []

if resistance is not None:

    tolerance = resistance * 0.005

    resistance_zone = [
        x for x in swing_highs
        if abs(x - resistance) <= tolerance
    ]

# ==========================================
# ZONA SUPPORTO
# ==========================================

support_zone = []

if support is not None:

    tolerance = support * 0.005

    support_zone = [
        x for x in swing_lows
        if abs(x - support) <= tolerance
    ]

# ==========================================
# LIMITI ZONE
# ==========================================

if resistance_zone:
    resistance_low = min(resistance_zone)
    resistance_high = max(resistance_zone)
else:
    resistance_low = resistance
    resistance_high = resistance

if support_zone:
    support_low = min(support_zone)
    support_high = max(support_zone)
else:
    support_low = support
    support_high = support

# ==========================================
# STATO OPERATIVO
# ==========================================

if price < ema20:

    signal = "🔴 NO LONG"
    reason = "Prezzo sotto EMA20"

else:

    signal = "🟡 ATTENDI"
    reason = "Trend rialzista ma nessun setup"

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

Zona Resistenza:
{resistance_low:.2f} - {resistance_high:.2f}

Zona Supporto:
{support_low:.2f} - {support_high:.2f}

STATO:
{signal}

Motivo:
{reason}
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

import os
import requests
import pandas as pd

from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

# ==========================================
# TELEGRAM
# ==========================================

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ==========================================
# COINS
# ==========================================

COINS = {
    "BTC": "XBTUSD",
    "ETH": "ETHUSD",
    "SOL": "SOLUSD",
    "LINK": "LINKUSD",
    "AVAX": "AVAXUSD"
}

watchlist = []
long_candidates = []

# ==========================================
# ANALISI
# ==========================================

for symbol, pair in COINS.items():

    try:

        response = requests.get(
            "https://api.kraken.com/0/public/OHLC",
            params={
                "pair": pair,
                "interval": 240
            },
            timeout=20
        )

        data = response.json()

        if "result" not in data:
            continue

        pair_name = None

        for key in data["result"].keys():
            if key != "last":
                pair_name = key
                break

        if pair_name is None:
            continue

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

        df["close"] = pd.to_numeric(df["close"])

        if len(df) < 200:
            continue

        # EMA

        df["ema20"] = EMAIndicator(
            close=df["close"],
            window=20
        ).ema_indicator()

        df["ema50"] = EMAIndicator(
            close=df["close"],
            window=50
        ).ema_indicator()

        df["ema200"] = EMAIndicator(
            close=df["close"],
            window=200
        ).ema_indicator()

        # RSI

        df["rsi"] = RSIIndicator(
            close=df["close"],
            window=14
        ).rsi()

        price = float(df.iloc[-1]["close"])
        ema20 = float(df.iloc[-1]["ema20"])
        ema50 = float(df.iloc[-1]["ema50"])
        ema200 = float(df.iloc[-1]["ema200"])
        rsi = float(df.iloc[-1]["rsi"])

        # ==================================
        # LONG CANDIDATE
        # ==================================

        if (
            price > ema20
            and ema20 > ema50
            and rsi > 55
        ):

            long_candidates.append(
                {
                    "symbol": symbol,
                    "price": price,
                    "rsi": rsi
                }
            )

        # ==================================
        # WATCHLIST
        # ==================================

        elif (
            price > ema20
            and rsi > 45
        ):

            watchlist.append(
                {
                    "symbol": symbol,
                    "price": price,
                    "rsi": rsi
                }
            )

        print(
            f"{symbol} | "
            f"P={price:.2f} "
            f"EMA20={ema20:.2f} "
            f"EMA50={ema50:.2f} "
            f"EMA200={ema200:.2f} "
            f"RSI={rsi:.2f}"
        )

    except Exception as e:

        print(f"Errore {symbol}: {e}")

# ==========================================
# MESSAGGIO TELEGRAM
# ==========================================

message = ""

if long_candidates:

    message += "🟢 LONG CANDIDATES\n\n"

    for coin in long_candidates:

        message += (
            f"{coin['symbol']}\n"
            f"Prezzo: {coin['price']:.2f}\n"
            f"RSI: {coin['rsi']:.1f}\n\n"
        )

if watchlist:

    message += "\n🟡 WATCHLIST\n\n"

    for coin in watchlist:

        message += (
            f"{coin['symbol']}\n"
            f"Prezzo: {coin['price']:.2f}\n"
            f"RSI: {coin['rsi']:.1f}\n\n"
        )

if message:

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )

    print(response.json())

else:

    print("Nessuna opportunità trovata")

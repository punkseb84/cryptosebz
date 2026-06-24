import os
import requests
import pandas as pd
from ta.trend import EMAIndicator

# TELEGRAM

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# COIN DA ANALIZZARE

COINS = {
    "BTC": "XBTUSD",
    "ETH": "ETHUSD",
    "SOL": "SOLUSD",
    "LINK": "LINKUSD",
    "AVAX": "AVAXUSD"
}

watchlist = []

# ANALISI

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
            print(f"{symbol}: nessun risultato")
            continue

        pair_name = None

        for key in data["result"].keys():
            if key != "last":
                pair_name = key
                break

        if pair_name is None:
            print(f"{symbol}: pair non trovata")
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
            print(f"{symbol}: dati insufficienti")
            continue

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

        price = float(df.iloc[-1]["close"])
        ema20 = float(df.iloc[-1]["ema20"])
        ema50 = float(df.iloc[-1]["ema50"])
        ema200 = float(df.iloc[-1]["ema200"])

        bull_trend = (
            price > ema20
            and ema20 > ema50
            and ema50 > ema200
        )

        if bull_trend:

            watchlist.append(
                {
                    "symbol": symbol,
                    "price": price,
                    "ema20": ema20,
                    "ema50": ema50,
                    "ema200": ema200
                }
            )

        print(
            f"{symbol} | "
            f"Price={price:.2f} "
            f"EMA20={ema20:.2f} "
            f"EMA50={ema50:.2f} "
            f"EMA200={ema200:.2f}"
        )

    except Exception as e:

        print(f"Errore {symbol}: {e}")

# TELEGRAM

if watchlist:

    message = "🟡 WATCHLIST 4H\n\n"

    for coin in watchlist:

        message += (
            f"{coin['symbol']}\n"
            f"Prezzo: {coin['price']:.2f}\n"
            f"EMA20: {coin['ema20']:.2f}\n"
            f"EMA50: {coin['ema50']:.2f}\n"
            f"EMA200: {coin['ema200']:.2f}\n\n"
        )

    telegram_url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    )

    response = requests.post(
        telegram_url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )

    print(response.json())

else:

    print("Nessuna coin in trend rialzista")

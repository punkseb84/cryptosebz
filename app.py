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
# COINS
# ==========================================

COINS = {
    "BTC": "XBTUSD",
    "ETH": "ETHUSD",
    "SOL": "SOLUSD",
    "LINK": "LINKUSD",
    "AVAX": "AVAXUSD"
}

signals = []

# ==========================================
# SCANNER
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

        for key in data["result"]:
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

        for col in ["open", "high", "low", "close"]:
            df[col] = pd.to_numeric(df[col])

        if len(df) < 220:
            continue

        # ==================================
        # EMA
        # ==================================

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

        # ==================================
        # PREZZI
        # ==================================

        close = float(df.iloc[-1]["close"])
        prev_close = float(df.iloc[-2]["close"])

        low = float(df.iloc[-1]["low"])

        ema20 = float(df.iloc[-1]["ema20"])
        ema50 = float(df.iloc[-1]["ema50"])
        ema200 = float(df.iloc[-1]["ema200"])

        # ==================================
        # TREND
        # ==================================

        bull_trend = (
            close > ema20
            and ema20 > ema50
            and ema50 > ema200
        )

        # ==================================
        # RESISTENZA
        # ultime 30 candele
        # esclusa quella attuale
        # ==================================

        resistance = (
            df["high"]
            .iloc[-31:-1]
            .max()
        )

        # ==================================
        # BREAKOUT
        # ==================================

        breakout = (
            prev_close <= resistance
            and close > resistance
        )

        # ==================================
        # LONG SETUP
        # ==================================

        if bull_trend and breakout:

            entry = close

            stop = low

            risk = entry - stop

            if risk <= 0:
                continue

            tp1 = entry + (risk * 2)
            tp2 = entry + (risk * 3)

            signals.append(
                {
                    "symbol": symbol,
                    "entry": entry,
                    "stop": stop,
                    "tp1": tp1,
                    "tp2": tp2,
                    "resistance": resistance
                }
            )

        print(
            f"{symbol} | "
            f"Close={close:.2f} "
            f"Res={resistance:.2f}"
        )

    except Exception as e:

        print(f"Errore {symbol}: {e}")

# ==========================================
# TELEGRAM
# ==========================================

if signals:

    message = "🟢 LONG SETUP TROVATO\n\n"

    for s in signals:

        message += (
            f"{s['symbol']}\n\n"
            f"Entry: {s['entry']:.2f}\n"
            f"Stop: {s['stop']:.2f}\n"
            f"TP1: {s['tp1']:.2f}\n"
            f"TP2: {s['tp2']:.2f}\n"
            f"Resistenza: {s['resistance']:.2f}\n\n"
        )

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

    print("Nessun LONG setup trovato")

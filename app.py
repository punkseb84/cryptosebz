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
    "XRP": "XRPUSD",
    "ADA": "ADAUSD",
    "DOGE": "DOGEUSD",
    "LINK": "LINKUSD",
    "AVAX": "AVAXUSD",
    "DOT": "DOTUSD",
    "LTC": "LTCUSD",
    "ATOM": "ATOMUSD",
    "UNI": "UNIUSD",
    "AAVE": "AAVEUSD",
    "FIL": "FILUSD",
    "ALGO": "ALGOUSD",
    "ICP": "ICPUSD",
    "APT": "APTUSD",
    "ARB": "ARBUSD",
    "OP": "OPUSD",
    "NEAR": "NEARUSD",
    "INJ": "INJUSD",
    "SUI": "SUIUSD",
    "SEI": "SEIUSD",
    "TIA": "TIAUSD",
    "JUP": "JUPUSD",
    "SHIB": "SHIBUSD",
    "PEPE": "PEPEUSD",
    "ETC": "ETCUSD",
    "BCH": "BCHUSD"
}

watchlist = []
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

        for col in ["open", "high", "low", "close", "volume"]:
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

        close = float(df.iloc[-1]["close"])
        open_price = float(df.iloc[-1]["open"])
        prev_close = float(df.iloc[-2]["close"])
        low = float(df.iloc[-1]["low"])

        ema20 = float(df.iloc[-1]["ema20"])
        ema50 = float(df.iloc[-1]["ema50"])
        ema200 = float(df.iloc[-1]["ema200"])

        bull_trend = (
            close > ema20
            and ema20 > ema50
            and ema50 > ema200
        )

        # ==================================
        # VOLUME
        # ==================================

        current_volume = float(df.iloc[-1]["volume"])
        avg_volume = float(df["volume"].tail(20).mean())

        if avg_volume > 0:
            rvol = current_volume / avg_volume
        else:
            rvol = 0

        # ==================================
        # SWING HIGHS
        # ==================================

        swing_highs = []

        for i in range(2, len(df) - 2):

            current_high = float(df.iloc[i]["high"])

            if (
                current_high > float(df.iloc[i - 1]["high"])
                and current_high > float(df.iloc[i - 2]["high"])
                and current_high > float(df.iloc[i + 1]["high"])
                and current_high > float(df.iloc[i + 2]["high"])
            ):
                swing_highs.append(current_high)

        resistances_above = [
            x for x in swing_highs
            if x > close
        ]

        if not resistances_above:
            continue

        valid_resistances = [
            x for x in resistances_above
            if ((x - close) / close) * 100 >= 1
        ]

        if not valid_resistances:
            continue

        resistance = min(valid_resistances)

        distance = (
            (resistance - close)
            / close
        ) * 100

        # ==================================
        # WATCHLIST
        # ==================================

        if distance <= 3:

            watchlist.append(
                {
                    "symbol": symbol,
                    "close": close,
                    "resistance": resistance,
                    "distance": distance,
                    "bull_trend": bull_trend,
                    "rvol": rvol
                }
            )

        # ==================================
        # BREAKOUT
        # ==================================

        breakout = (
            prev_close <= resistance
            and close > resistance
            and close > open_price
        )

        # ==================================
        # LONG SETUP
        # ==================================

        if bull_trend and breakout and rvol > 1.2:

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
                    "resistance": resistance,
                    "rvol": rvol
                }
            )

        print(
            f"{symbol} | "
            f"Close={close:.2f} "
            f"Res={resistance:.2f} "
            f"Dist={distance:.2f}% "
            f"RVOL={rvol:.2f}"
        )

    except Exception as e:

        print(f"Errore {symbol}: {e}")

# ==========================================
# TELEGRAM
# ==========================================

message = ""

if signals:

    message += "🟢 LONG SETUP\n\n"

    for s in signals:

        message += (
            f"{s['symbol']}\n"
            f"Entry: {s['entry']:.2f}\n"
            f"Stop: {s['stop']:.2f}\n"
            f"TP1: {s['tp1']:.2f}\n"
            f"TP2: {s['tp2']:.2f}\n"
            f"RVOL: {s['rvol']:.2f}\n\n"
        )

if watchlist:

    message += "🟡 WATCHLIST\n\n"

    for w in watchlist:

        trend_text = (
            "RIALZISTA"
            if w["bull_trend"]
            else "NON RIALZISTA"
        )

        message += (
            f"{w['symbol']}\n"
            f"Prezzo: {w['close']:.2f}\n"
            f"Resistenza: {w['resistance']:.2f}\n"
            f"Distanza: {w['distance']:.2f}%\n"
            f"Trend: {trend_text}\n"
            f"RVOL: {w['rvol']:.2f}\n\n"
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

    print("Nessun setup trovato")

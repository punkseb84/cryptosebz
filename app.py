import os
import requests
import pandas as pd

from ta.trend import EMAIndicator

pre_long = []

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

        # Ultima candela 4H CHIUSA
        close = float(df.iloc[-2]["close"])
        open_price = float(df.iloc[-2]["open"])
        low = float(df.iloc[-2]["low"])

        # Candela chiusa precedente
        prev_close = float(df.iloc[-3]["close"])

        ema20 = float(df.iloc[-2]["ema20"])
        ema50 = float(df.iloc[-2]["ema50"])
        ema200 = float(df.iloc[-2]["ema200"])

        trend_score = 0

        if close > ema20:
            trend_score += 1

        if ema20 > ema50:
            trend_score += 1

        if ema50 > ema200:
            trend_score += 1

        bull_trend = (trend_score == 3)

        # ==================================
        # VOLUME
        # ==================================

        # Volume dell'ultima candela CHIUSA
        current_volume = float(df.iloc[-2]["volume"])

        # Media delle 20 candele chiuse precedenti
        avg_volume = float(
            df["volume"].iloc[-22:-2].mean()
        )

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

        if pre_long:

            message += "🟠 PRE-LONG\n\n"

            for p in pre_long:

                message += (
                f"{p['symbol']}\n"
                f"Score: {p['score']:.1f}\n"
                f"Trend Score: {p['trend_score']}/3\n"
                f"Distanza: {p['distance']:.2f}%\n"
                f"RVOL: {p['rvol']:.2f}\n\n"
        )

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
    "trend_score": trend_score,
    "rvol": rvol,
    "score": score
}
            )

        score = (
        trend_score * 50
        + rvol * 20
        - distance * 5
)

        if (
        trend_score >= 2
        and rvol > 1.2
        and distance <= 2
):
    pre_long.append(
        {
            "symbol": symbol,
            "close": close,
            "distance": distance,
            "trend_score": trend_score,
            "rvol": rvol,
            "score": score
        }
    )

        # ==================================
        # BREAKOUT
        # ==================================

        breakout = (
            prev_close <= resistance
            and close > resistance * 1.005
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
            f"(4H CLOSED)"
        )

    except Exception as e:

        print(f"Errore {symbol}: {e}")

watchlist = sorted(
    watchlist,
    key=lambda x: x["score"],
    reverse=True
)[:5]

pre_long = sorted(
    pre_long,
    key=lambda x: x["score"],
    reverse=True
)[:5]

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

trend_text = f"{w['trend_score']}/3"

        message += (
            f"{w['symbol']}\n"
            f"Prezzo: {w['close']:.2f}\n"
            f"Resistenza: {w['resistance']:.2f}\n"
            f"Distanza: {w['distance']:.2f}%\n"
            f"Trend Score: {trend_text}\n"
            f"Score: {w['score']:.1f}\n"
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

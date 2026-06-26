# ==========================================================
# UTILS
# ==========================================================

import requests
import pandas as pd

from config import KRAKEN_URL, TIMEFRAME_MAIN


# ==========================================================
# DOWNLOAD OHLC DA KRAKEN
# ==========================================================

def get_ohlc(pair, interval=TIMEFRAME_MAIN):
    response = requests.get(
        KRAKEN_URL,
        params={
            "pair": pair,
            "interval": interval,
        },
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()

    if data.get("error"):
        raise Exception(f"Kraken API Error: {data['error']}")

    if "result" not in data:
        raise Exception("Risposta Kraken non valida")

    pair_name = None

    for key in data["result"]:
        if key != "last":
            pair_name = key
            break

    if pair_name is None:
        raise Exception("Pair non trovato")

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
            "count",
        ],
    )

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["time"] = pd.to_numeric(df["time"], errors="coerce")
    df = df.dropna()

    if df.empty:
        raise Exception("Nessun dato OHLC ricevuto")

    return df


# ==========================================================
# CONTROLLO STORICO
# ==========================================================

def enough_history(df, minimum=220):
    return len(df) >= minimum


# ==========================================================
# LOG
# ==========================================================

def log(symbol, message):
    print(f"[{symbol}] {message}")


# ==========================================================
# FORMAT PREZZO
# ==========================================================

def price(value):
    if value is None:
        return "-"

    return f"{value:.2f}"


# ==========================================================
# COMPATIBILITÀ MODULI LEGACY
# ==========================================================

def last_closed(df):
    return df.iloc[-2]


def previous_closed(df):
    return df.iloc[-3]


def percent(value):
    if value is None:
        return "-"

    return f"{value:.2f}%"

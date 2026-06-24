import requests
import pandas as pd

from config import (
    KRAKEN_URL,
    INTERVAL
)


# ==========================================================
# DOWNLOAD OHLC DA KRAKEN
# ==========================================================

def get_ohlc(pair):

    response = requests.get(
        KRAKEN_URL,
        params={
            "pair": pair,
            "interval": INTERVAL
        },
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

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
            "count"
        ]
    )

    for col in [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]:

        df[col] = pd.to_numeric(df[col])

    return df


# ==========================================================
# CONTROLLA NUMERO CANDELE
# ==========================================================

def enough_history(df, minimum=220):

    return len(df) >= minimum


# ==========================================================
# ULTIMA CANDELA 4H CHIUSA
# ==========================================================

def last_closed(df):

    return df.iloc[-2]


# ==========================================================
# CANDELA PRECEDENTE
# ==========================================================

def previous_closed(df):

    return df.iloc[-3]


# ==========================================================
# STAMPA LOG
# ==========================================================

def log(symbol, message):

    print(f"[{symbol}] {message}")


# ==========================================================
# FORMATTA PREZZO
# ==========================================================

def price(value):

    return f"{value:.2f}"


# ==========================================================
# FORMATTA PERCENTUALE
# ==========================================================

def percent(value):

    return f"{value:.2f}%"
# ==========================================================
# UTILS
# V6.1
# ==========================================================

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

    # ------------------------------------------------------
    # Controllo errori Kraken
    # ------------------------------------------------------

    if data.get("error"):

        raise Exception(
            f"Kraken API Error: {data['error']}"
        )

    if "result" not in data:

        raise Exception(
            "Risposta Kraken non valida"
        )

    # ------------------------------------------------------
    # Individua il nome reale della coppia
    # ------------------------------------------------------

    pair_name = None

    for key in data["result"]:

        if key != "last":

            pair_name = key

            break

    if pair_name is None:

        raise Exception(
            "Pair non trovato"
        )

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

    # ------------------------------------------------------
    # Conversione numerica
    # ------------------------------------------------------

    numeric_columns = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # ------------------------------------------------------
    # Rimuove eventuali valori NaN
    # ------------------------------------------------------

    df = df.dropna()

    if df.empty:

        raise Exception(
            "Nessun dato OHLC ricevuto"
        )

    return df


# ==========================================================
# CONTROLLO STORICO
# ==========================================================

def enough_history(

    df,

    minimum=220

):

    return len(df) >= minimum


# ==========================================================
# ULTIMA CANDELA CHIUSA
# ==========================================================

def last_closed(df):

    return df.iloc[-2]


# ==========================================================
# CANDELA PRECEDENTE
# ==========================================================

def previous_closed(df):

    return df.iloc[-3]


# ==========================================================
# LOG
# ==========================================================

def log(

    symbol,

    message

):

    print(

        f"[{symbol}] {message}"

    )


# ==========================================================
# FORMAT PREZZO
# ==========================================================

def price(value):

    if value is None:

        return "-"

    return f"{value:.2f}"


# ==========================================================
# FORMAT PERCENTUALE
# ==========================================================

def percent(value):

    if value is None:

        return "-"

    return f"{value:.2f}%"


# ==========================================================
# FORMAT RVOL
# ==========================================================

def rvol(value):

    if value is None:

        return "-"

    return f"{value:.2f}"


# ==========================================================
# DEBUG DATAFRAME
# ==========================================================

def debug_dataframe(df):

    print()

    print("=" * 60)

    print(df.tail())

    print("=" * 60)

    print()

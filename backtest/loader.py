# ==========================================================
# LOADER
# V1.0
# ==========================================================

import os
import requests
import pandas as pd

from config import (
    KRAKEN_URL,
    INTERVAL
)

# ==========================================================
# CARTELLA DATI
# ==========================================================

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)


# ==========================================================
# FILE LOCALE
# ==========================================================

def history_file(symbol):

    return os.path.join(

        DATA_DIR,

        f"{symbol}_4H.csv"

    )


# ==========================================================
# ESISTE?
# ==========================================================

def history_exists(symbol):

    return os.path.exists(

        history_file(symbol)

    )


# ==========================================================
# CARICA CSV
# ==========================================================

def load_local(symbol):

    df = pd.read_csv(

        history_file(symbol)

    )

    return df


# ==========================================================
# SALVA CSV
# ==========================================================

def save_local(symbol, df):

    df.to_csv(

        history_file(symbol),

        index=False

    )


# ==========================================================
# DOWNLOAD KRAKEN
# ==========================================================

def download_history(pair):

    response = requests.get(

        KRAKEN_URL,

        params={

            "pair": pair,

            "interval": INTERVAL

        },

        timeout=30

    )

    response.raise_for_status()

    data = response.json()

    if "result" not in data:

        raise Exception("Kraken error")

    pair_name = None

    for key in data["result"]:

        if key != "last":

            pair_name = key

            break

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

    numeric = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]

    for col in numeric:

        df[col] = pd.to_numeric(df[col])

    return df


# ==========================================================
# LOAD HISTORY
# ==========================================================

def load_history(

    symbol,

    pair

):

    if history_exists(symbol):

        print(f"{symbol}: storico locale")

        return load_local(symbol)

    print(f"{symbol}: download Kraken")

    df = download_history(pair)

    save_local(symbol, df)

    return df

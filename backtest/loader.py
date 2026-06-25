# ==========================================================
# LOADER
# BACKTEST V1
# ==========================================================

import pandas as pd

from utils import get_ohlc


# ==========================================================
# CARICA STORICO
# ==========================================================

def load_history(pair):

    print(f"Download storico {pair}...")

    df = get_ohlc(pair)

    print(f"Candele scaricate: {len(df)}")

    return df


# ==========================================================
# INFO
# ==========================================================

def print_history(df):

    print()

    print("Prime 5 candele")

    print(df.head())

    print()

    print("Ultime 5 candele")

    print(df.tail())

    print()

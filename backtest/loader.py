# ==========================================================
# LOADER
# V1.0
# ==========================================================

import os
import pandas as pd

from config import COINS


# ==========================================================
# CARTELLA DATI
# ==========================================================

DATA_DIR = "data"


# ==========================================================
# CREA CARTELLA
# ==========================================================

def create_data_folder():

    os.makedirs(

        DATA_DIR,

        exist_ok=True

    )


# ==========================================================
# PERCORSO FILE
# ==========================================================

def history_path(symbol):

    return os.path.join(

        DATA_DIR,

        f"{symbol}_4H.csv"

    )


# ==========================================================
# FILE ESISTE
# ==========================================================

def history_exists(symbol):

    return os.path.exists(

        history_path(symbol)

    )


# ==========================================================
# CARICA CSV
# ==========================================================

def load_local(symbol):

    return pd.read_csv(

        history_path(symbol)

    )


# ==========================================================
# SALVA CSV
# ==========================================================

def save_local(

    symbol,

    df

):

    create_data_folder()

    df.to_csv(

        history_path(symbol),

        index=False

    )


# ==========================================================
# DEBUG
# ==========================================================

def print_loader(

    symbol,

    rows

):

    print(

        f"{symbol}"

        f" | "

        f"{rows}"

        f" candles"

    )

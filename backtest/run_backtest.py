# ==========================================================
# CRYPTO SCANNER
# BACKTEST V1
# ==========================================================

from datetime import datetime

from backtest.loader import (
    load_history,
    print_history
)

from config import COINS


# ==========================================================
# MAIN
# ==========================================================

def main():

    print()

    print("=" * 60)
    print("CRYPTO SCANNER BACKTEST V1")
    print("=" * 60)

    print(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

    print()

    # BTC
    pair = COINS["BTC"]

    df = load_history(pair)

    print_history(df)

    print("=" * 60)


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":

    main()

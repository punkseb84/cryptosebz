# ==========================================================
# TRADE
# V1.0
# ==========================================================

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# ==========================================================
# TRADE
# ==========================================================

@dataclass
class Trade:

    # ----------------------------------------------
    # IDENTIFICAZIONE
    # ----------------------------------------------

    symbol: str

    # ----------------------------------------------
    # INGRESSO
    # ----------------------------------------------

    entry_time: datetime

    entry_price: float

    stop_loss: float

    take_profit_1: float

    take_profit_2: float

    # ----------------------------------------------
    # USCITA
    # ----------------------------------------------

    exit_time: Optional[datetime] = None

    exit_price: Optional[float] = None

    exit_reason: Optional[str] = None

    # ----------------------------------------------
    # RISULTATI
    # ----------------------------------------------

    risk: float = 0.0

    reward: float = 0.0

    rr: float = 0.0

    profit: float = 0.0

    profit_percent: float = 0.0

    # ----------------------------------------------
    # STATO
    # ----------------------------------------------

    status: str = "OPEN"

    hit_tp1: bool = False

    hit_tp2: bool = False

    hit_stop: bool = False

    # ======================================================
    # CHIUDE IL TRADE
    # ======================================================

    def close(

        self,

        price: float,

        time: datetime,

        reason: str

    ):

        self.exit_price = price

        self.exit_time = time

        self.exit_reason = reason

        self.status = "CLOSED"

        self.profit = price - self.entry_price

        self.profit_percent = (

            self.profit

            / self.entry_price

        ) * 100

    # ======================================================
    # DEBUG
    # ======================================================

    def __str__(self):

        return (

            f"{self.symbol} | "

            f"Entry={self.entry_price:.2f} | "

            f"Exit={self.exit_price} | "

            f"Status={self.status}"

        )

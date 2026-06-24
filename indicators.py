# ==========================================================
# INDICATORS
# V6.1
# ==========================================================

import pandas as pd

from ta.trend import EMAIndicator

from config import (
    EMA_FAST,
    EMA_MID,
    EMA_SLOW,
    RVOL_PERIOD,
    RVOL_CAP
)


# ==========================================================
# AGGIUNGE EMA
# ==========================================================

def add_ema(df):

    df["ema20"] = EMAIndicator(
        close=df["close"],
        window=EMA_FAST
    ).ema_indicator()

    df["ema50"] = EMAIndicator(
        close=df["close"],
        window=EMA_MID
    ).ema_indicator()

    df["ema200"] = EMAIndicator(
        close=df["close"],
        window=EMA_SLOW
    ).ema_indicator()

    return df


# ==========================================================
# RVOL
# ==========================================================

def calculate_rvol(df):

    current_volume = float(
        df.iloc[-2]["volume"]
    )

    avg_volume = float(
        df["volume"]
        .iloc[-(RVOL_PERIOD + 2):-2]
        .mean()
    )

    if avg_volume <= 0:

        return 0.0

    rvol = current_volume / avg_volume

    return min(rvol, RVOL_CAP)


# ==========================================================
# TREND SCORE
# ==========================================================

def calculate_trend_score(df):

    close = float(df.iloc[-2]["close"])

    ema20 = float(df.iloc[-2]["ema20"])
    ema50 = float(df.iloc[-2]["ema50"])
    ema200 = float(df.iloc[-2]["ema200"])

    score = 0

    if close > ema20:
        score += 1

    if ema20 > ema50:
        score += 1

    if ema50 > ema200:
        score += 1

    return score


# ==========================================================
# BULL TREND
# ==========================================================

def bull_trend(trend_score):

    return trend_score == 3


# ==========================================================
# TREND ACCETTABILE
# ==========================================================

def acceptable_trend(trend_score):

    return trend_score >= 2


# ==========================================================
# ULTIMA CANDELA CHIUSA
# ==========================================================

def last_candle(df):

    candle = df.iloc[-2]

    return {

        "open": float(candle["open"]),

        "high": float(candle["high"]),

        "low": float(candle["low"]),

        "close": float(candle["close"]),

        "volume": float(candle["volume"])

    }


# ==========================================================
# CHIUSURA PRECEDENTE
# ==========================================================

def previous_close(df):

    return float(df.iloc[-3]["close"])


# ==========================================================
# DEBUG EMA
# ==========================================================

def print_trend(

    symbol,

    trend_score,

    rvol

):

    print(

        f"[{symbol}] "

        f"Trend={trend_score}/3 "

        f"RVOL={rvol:.2f}"

    )

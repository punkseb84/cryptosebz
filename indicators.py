# ==========================================================
# INDICATORS
# ==========================================================

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange

from config import (
    ATR_PERIOD,
    EMA_FAST,
    EMA_MID,
    EMA_SLOW,
    MACD_FAST,
    MACD_SIGNAL,
    MACD_SLOW,
    RSI_PERIOD,
    VOLUME_PERIOD,
)


# ==========================================================
# INDICATORI TECNICI
# ==========================================================

def add_indicators(df):
    df = df.copy()

    df["ema20"] = EMAIndicator(close=df["close"], window=EMA_FAST).ema_indicator()
    df["ema50"] = EMAIndicator(close=df["close"], window=EMA_MID).ema_indicator()
    df["ema200"] = EMAIndicator(close=df["close"], window=EMA_SLOW).ema_indicator()
    df["rsi"] = RSIIndicator(close=df["close"], window=RSI_PERIOD).rsi()

    macd = MACD(
        close=df["close"],
        window_fast=MACD_FAST,
        window_slow=MACD_SLOW,
        window_sign=MACD_SIGNAL,
    )
    df["macd_hist"] = macd.macd_diff()

    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=ATR_PERIOD,
    )
    df["atr"] = atr.average_true_range()

    return df


# Backward-compatible alias for older modules.
def add_ema(df):
    return add_indicators(df)


# ==========================================================
# CANDELE CHIUSE
# ==========================================================

def last_candle(df):
    candle = df.iloc[-2]

    return {
        "time": int(candle["time"]),
        "open": float(candle["open"]),
        "high": float(candle["high"]),
        "low": float(candle["low"]),
        "close": float(candle["close"]),
        "volume": float(candle["volume"]),
        "ema20": float(candle["ema20"]),
        "ema50": float(candle["ema50"]),
        "ema200": float(candle["ema200"]),
        "rsi": float(candle["rsi"]),
        "macd_hist": float(candle["macd_hist"]),
        "atr": float(candle["atr"]),
    }


def previous_candle(df):
    candle = df.iloc[-3]

    return {
        "close": float(candle["close"]),
        "macd_hist": float(candle["macd_hist"]),
    }


# ==========================================================
# VOLUME
# ==========================================================

def average_volume(df, period=VOLUME_PERIOD):
    return float(df["volume"].iloc[-(period + 2):-2].mean())


# ==========================================================
# TREND SCORE LEGACY
# ==========================================================

def calculate_trend_score(df):
    candle = last_candle(df)
    score = 0

    if candle["close"] > candle["ema20"]:
        score += 1

    if candle["ema20"] > candle["ema50"]:
        score += 1

    if candle["ema50"] > candle["ema200"]:
        score += 1

    return score


def calculate_rvol(df):
    current_volume = last_candle(df)["volume"]
    avg_volume = average_volume(df)

    if avg_volume <= 0:
        return 0.0

    return current_volume / avg_volume


def previous_close(df):
    return float(df.iloc[-3]["close"])

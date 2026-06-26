# ==========================================================
# SIGNALS
# ==========================================================

from config import (
    ATR_STOP_MULTIPLIER,
    LONG_RSI_MAX,
    LONG_RSI_MIN,
    MIN_VOLUME_RATIO,
    NEAR_LEVEL_PERCENT,
    SHORT_RSI_MAX,
    SHORT_RSI_MIN,
    SUPPORT_RESISTANCE_PERIOD,
    TP1_RR,
    TP2_RR,
)


# ==========================================================
# SUPPORTI / RESISTENZE / BREAKOUT
# ==========================================================

def support_resistance(df, period=SUPPORT_RESISTANCE_PERIOD):
    closed = df.iloc[-(period + 1):-1]

    return float(closed["low"].min()), float(closed["high"].max())


def previous_support_resistance(df, period=SUPPORT_RESISTANCE_PERIOD):
    previous = df.iloc[-(period + 2):-2]

    return float(previous["low"].min()), float(previous["high"].max())


def near_level(price, level, max_distance_percent=NEAR_LEVEL_PERCENT):
    if level <= 0:
        return False

    distance = abs(price - level) / level * 100
    return distance <= max_distance_percent


def long_breakout(close, previous_resistance):
    return close > previous_resistance


def short_breakdown(close, previous_support):
    return close < previous_support


# ==========================================================
# CONDIZIONI LONG / SHORT
# ==========================================================

def long_conditions(candle_5m, previous_5m, candle_15m, candle_1h, avg_volume, support, previous_resistance):
    return {
        "trend_1h": candle_1h["close"] > candle_1h["ema200"] or candle_1h["ema50"] > candle_1h["ema200"],
        "trend_15m": candle_15m["close"] > candle_15m["ema50"],
        "ema_5m": candle_5m["ema20"] > candle_5m["ema50"],
        "rsi": LONG_RSI_MIN <= candle_5m["rsi"] <= LONG_RSI_MAX,
        "macd": candle_5m["macd_hist"] > 0 or candle_5m["macd_hist"] > previous_5m["macd_hist"],
        "volume": avg_volume > 0 and candle_5m["volume"] > MIN_VOLUME_RATIO * avg_volume,
        "level": near_level(candle_5m["close"], support) or long_breakout(candle_5m["close"], previous_resistance),
    }


def short_conditions(candle_5m, previous_5m, candle_15m, candle_1h, avg_volume, resistance, previous_support):
    return {
        "trend_1h": candle_1h["close"] < candle_1h["ema200"] or candle_1h["ema50"] < candle_1h["ema200"],
        "trend_15m": candle_15m["close"] < candle_15m["ema50"],
        "ema_5m": candle_5m["ema20"] < candle_5m["ema50"],
        "rsi": SHORT_RSI_MIN <= candle_5m["rsi"] <= SHORT_RSI_MAX,
        "macd": candle_5m["macd_hist"] < 0 or candle_5m["macd_hist"] < previous_5m["macd_hist"],
        "volume": avg_volume > 0 and candle_5m["volume"] > MIN_VOLUME_RATIO * avg_volume,
        "level": near_level(candle_5m["close"], resistance) or short_breakdown(candle_5m["close"], previous_support),
    }


def all_conditions_met(conditions):
    return all(conditions.values())


# ==========================================================
# RISK MANAGEMENT
# ==========================================================

def build_signal(symbol, direction, entry, atr, candle_time):
    risk = ATR_STOP_MULTIPLIER * atr

    if risk <= 0:
        return None

    if direction == "LONG":
        stop = entry - risk
        tp1 = entry + TP1_RR * risk
        tp2 = entry + TP2_RR * risk
    else:
        stop = entry + risk
        tp1 = entry - TP1_RR * risk
        tp2 = entry - TP2_RR * risk

    return {
        "symbol": symbol,
        "direction": direction,
        "entry": entry,
        "stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "timeframe": "5m",
        "candle_time": candle_time,
    }

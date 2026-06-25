# ==========================================================
# BACKTEST ENGINE
# ==========================================================

from copy import deepcopy
from itertools import product

from indicators import (
    add_ema,
    calculate_rvol,
    calculate_trend_score,
    last_candle,
    previous_close,
)
from backtest.metrics import calculate_metrics
from patterns import (
    breakout as is_breakout_pattern,
    distance_percent,
    find_swing_highs,
    find_swing_lows,
    nearest_support,
    valid_resistance,
)
from signals import build_long_signal, is_long


DEFAULT_RVOL_VALUES = (1.0, 1.2, 1.5, 2.0)
DEFAULT_PRELONG_VALUES = (0.75, 1.0, 1.5, 2.0, 3.0)
DEFAULT_BREAKOUT_VALUES = (0.0025, 0.005, 0.0075, 0.01)


def _prepare_history(df):

    history = deepcopy(df)
    history = history.sort_values("time") if "time" in history.columns else history
    history = history.reset_index(drop=True)

    return add_ema(history)


def _time_value(row):

    value = row.get("time") if hasattr(row, "get") else None

    return value


def _build_signal(symbol, window, rvol_min, prelong_distance, breakout_buffer):

    candle = last_candle(window)

    close = candle["close"]
    open_price = candle["open"]
    low = candle["low"]

    prev_close = previous_close(window)
    trend_score = calculate_trend_score(window)
    rvol = calculate_rvol(window)

    swing_highs = find_swing_highs(window)
    swing_lows = find_swing_lows(window)

    resistance = valid_resistance(
        close,
        swing_highs
    )

    if resistance is None:
        return None

    distance = distance_percent(
        close,
        resistance
    )

    if distance is None or distance > prelong_distance:
        return None

    support = nearest_support(
        close,
        swing_lows
    )

    signal_breakout = is_breakout_pattern(
        previous_close=prev_close,
        current_close=close,
        current_open=open_price,
        resistance=resistance,
        buffer=breakout_buffer,
    )

    if not is_long(
        trend_score=trend_score,
        breakout=signal_breakout,
        rvol=rvol,
        rvol_min=rvol_min,
    ):
        return None

    return build_long_signal(
        symbol=symbol,
        entry=close,
        support=support,
        candle_low=low,
        resistance=resistance,
        rvol=rvol,
        trend_score=trend_score,
    )


def _simulate_exit(df, start_index, signal):

    entry = float(signal["entry"])
    stop = float(signal["stop"])
    tp1 = float(signal["tp1"])
    tp2 = float(signal["tp2"])

    for index in range(start_index, len(df)):
        row = df.iloc[index]
        low = float(row["low"])
        high = float(row["high"])
        exit_time = _time_value(row)

        if low <= stop:
            return index, stop, exit_time, "STOP"

        if high >= tp2:
            return index, tp2, exit_time, "TP2"

        if high >= tp1:
            return index, tp1, exit_time, "TP1"

    row = df.iloc[-1]

    return len(df) - 1, float(row["close"]), _time_value(row), "END"


def run_backtest(
    symbol,
    df,
    rvol_min,
    prelong_distance,
    breakout_buffer,
    warmup=220,
):

    history = _prepare_history(df)
    trades = []
    index = max(warmup, 3)

    while index < len(history) - 1:
        window = history.iloc[:index + 1].copy()
        signal = _build_signal(
            symbol=symbol,
            window=window,
            rvol_min=rvol_min,
            prelong_distance=prelong_distance,
            breakout_buffer=breakout_buffer,
        )

        if signal is None:
            index += 1
            continue

        exit_index, exit_price, exit_time, exit_reason = _simulate_exit(
            history,
            index + 1,
            signal,
        )

        entry_time = _time_value(history.iloc[index - 1])
        entry = float(signal["entry"])
        profit = exit_price - entry

        trades.append({
            "symbol": symbol,
            "entry_time": entry_time,
            "entry": entry,
            "stop": float(signal["stop"]),
            "tp1": float(signal["tp1"]),
            "tp2": float(signal["tp2"]),
            "exit_time": exit_time,
            "exit": exit_price,
            "exit_reason": exit_reason,
            "profit": profit,
            "profit_percent": (profit / entry) * 100,
            "rvol": float(signal["rvol"]),
            "trend_score": int(signal["trend_score"]),
            "resistance": float(signal["resistance"]),
            "rvol_min": rvol_min,
            "prelong_distance": prelong_distance,
            "breakout_buffer": breakout_buffer,
        })

        index = exit_index + 1

    metrics = calculate_metrics(trades)

    return {
        "symbol": symbol,
        "trades": trades,
        "metrics": metrics,
    }


def grid_search(
    symbol,
    df,
    rvol_values=DEFAULT_RVOL_VALUES,
    prelong_values=DEFAULT_PRELONG_VALUES,
    breakout_values=DEFAULT_BREAKOUT_VALUES,
):

    results = []

    for rvol_min, prelong_distance, breakout_buffer in product(
        rvol_values,
        prelong_values,
        breakout_values,
    ):
        backtest = run_backtest(
            symbol=symbol,
            df=df,
            rvol_min=rvol_min,
            prelong_distance=prelong_distance,
            breakout_buffer=breakout_buffer,
        )

        metrics = backtest["metrics"]
        results.append({
            "symbol": symbol,
            "rvol_min": rvol_min,
            "prelong_distance": prelong_distance,
            "breakout_buffer": breakout_buffer,
            "profit_factor": metrics["profit_factor"],
            "win_rate": metrics["win_rate"],
            "net_profit": metrics["net_profit"],
            "max_drawdown": metrics["max_drawdown"],
            "trade_count": metrics["trade_count"],
        })

    return sorted(
        results,
        key=lambda row: (
            row["profit_factor"],
            row["net_profit"],
            row["trade_count"],
        ),
        reverse=True,
    )

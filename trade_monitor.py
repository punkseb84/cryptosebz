"""Monitor open trades against subsequent Kraken OHLC candles."""

from __future__ import annotations

from datetime import datetime, timezone

from config import COINS, TIMEFRAME_MAIN
from trade_history import STATUS_SL, STATUS_TP1, TradeHistory, calculate_profit
from utils import get_ohlc, log


def monitor_open_trades(history=None):
    history = history or TradeHistory()
    updated = 0

    for trade in history.open_trades():
        symbol = trade.get("symbol")
        pair = COINS.get(symbol)
        if not pair:
            continue

        try:
            df = get_ohlc(pair, interval=TIMEFRAME_MAIN)
            result = evaluate_trade(trade, df)
            if result:
                history.update(trade["id"], **result)
                updated += 1
        except Exception as exc:
            log(symbol, f"Errore monitoraggio trade: {exc}")

    return updated


def evaluate_trade(trade, df):
    candle_time = int(trade["candle_time"])
    following = df[df["time"] > candle_time].sort_values("time")

    if following.empty:
        return None

    direction = trade.get("direction", "LONG")
    target_1 = float(trade["target_1"])
    stop_loss = float(trade["stop_loss"])

    for candle in following.to_dict("records"):
        high = float(candle["high"])
        low = float(candle["low"])

        if direction == "LONG":
            hit_tp1 = high >= target_1
            hit_sl = low <= stop_loss
        else:
            hit_tp1 = low <= target_1
            hit_sl = high >= stop_loss

        if hit_tp1 and hit_sl:
            return close_result(trade, STATUS_SL, stop_loss, candle["time"])
        if hit_tp1:
            return close_result(trade, STATUS_TP1, target_1, candle["time"])
        if hit_sl:
            return close_result(trade, STATUS_SL, stop_loss, candle["time"])

    return None


def close_result(trade, status, exit_price, candle_time):
    closed_at = datetime.fromtimestamp(int(candle_time), tz=timezone.utc).isoformat()
    return {
        "status": status,
        "closed_at": closed_at,
        "exit_price": float(exit_price),
        "profit_eur": calculate_profit(trade, exit_price),
    }

"""Persistent trade archive for generated crypto bot signals."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile

from config import TRADE_HISTORY_FILE

STATUS_OPEN = "OPEN"
STATUS_TP1 = "TP1"
STATUS_SL = "SL"
INITIAL_CAPITAL_EUR = 10.0


class TradeHistory:
    def __init__(self, path=TRADE_HISTORY_FILE):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def all(self):
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        return data if isinstance(data, list) else []

    def add_signal(self, signal, reasons):
        trades = self.all()
        trade = build_trade(signal, reasons, investment_eur=current_compound_capital(trades))

        if any(existing.get("id") == trade["id"] for existing in trades):
            return False

        trades.append(trade)
        self._write(trades)
        return True

    def update(self, trade_id, **fields):
        trades = self.all()
        updated = False

        for trade in trades:
            if trade.get("id") == trade_id:
                trade.update(fields)
                updated = True
                break

        if updated:
            self._write(trades)

        return updated

    def open_trades(self):
        return [trade for trade in self.all() if trade.get("status") == STATUS_OPEN]

    def _write(self, trades):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile("w", encoding="utf-8", dir=self.path.parent, delete=False) as handle:
            json.dump(trades, handle, ensure_ascii=False, indent=2, sort_keys=True)
            temp_name = handle.name

        os.replace(temp_name, self.path)


def build_trade(signal, reasons, investment_eur=INITIAL_CAPITAL_EUR):
    candle_time = int(signal["candle_time"])
    created_at = datetime.fromtimestamp(candle_time, tz=timezone.utc).isoformat()
    symbol = signal["symbol"]
    direction = signal["direction"]

    return {
        "id": f"{symbol}-{direction}-{candle_time}",
        "created_at": created_at,
        "candle_time": candle_time,
        "symbol": symbol,
        "pair": f"{symbol}/USD",
        "direction": direction,
        "investment_eur": round(float(investment_eur), 4),
        "entry": float(signal["entry"]),
        "stop_loss": float(signal["stop"]),
        "target_1": float(signal["tp1"]),
        "target_2": float(signal["tp2"]),
        "timeframe": signal.get("timeframe", "5m"),
        "reasons": list(reasons),
        "status": STATUS_OPEN,
        "closed_at": None,
        "exit_price": None,
        "profit_eur": 0.0,
    }


def calculate_profit(trade, exit_price):
    entry = float(trade["entry"])
    if entry <= 0:
        return 0.0

    direction = trade.get("direction", "LONG")
    change = (float(exit_price) - entry) / entry
    if direction == "SHORT":
        change *= -1

    investment_eur = float(trade.get("investment_eur", INITIAL_CAPITAL_EUR))
    return round(investment_eur * change, 4)


def current_compound_capital(trades):
    capital = INITIAL_CAPITAL_EUR

    for trade in sorted(
        trades,
        key=lambda item: item.get("closed_at") or item.get("created_at", ""),
    ):
        if trade.get("status") in {STATUS_TP1, STATUS_SL}:
            capital += float(trade.get("profit_eur", 0.0))

    return round(max(capital, 0.0), 4)

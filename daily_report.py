"""Build and send daily Telegram performance reports."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram_bot import send_message
from trade_history import INVESTMENT_EUR, STATUS_OPEN, STATUS_SL, STATUS_TP1, TradeHistory

ROME_TZ = ZoneInfo("Europe/Rome")


def send_daily_report(history=None, now=None):
    history = history or TradeHistory()
    message = build_daily_report(history.all(), now=now)
    send_message(message)
    return message


def build_daily_report(trades, now=None):
    now = now or datetime.now(ROME_TZ)
    if now.tzinfo is None:
        now = now.replace(tzinfo=ROME_TZ)

    since = now - timedelta(hours=24)
    recent = [trade for trade in trades if _created_at(trade) >= since]

    recent_stats = _stats(recent)
    total_stats = _stats(trades)
    recent_lines = _format_recent_trades(recent)

    return (
        "📊 REPORT GIORNALIERO BOT CRYPTO\n\n"
        "Ultime 24 ore\n"
        f"Segnali: {recent_stats['total']}\n"
        f"TP1: {recent_stats['tp1']}\n"
        f"SL: {recent_stats['sl']}\n"
        f"OPEN: {recent_stats['open']}\n\n"
        "Storico completo\n"
        f"Segnali totali: {total_stats['total']}\n"
        f"TP1: {total_stats['tp1']}\n"
        f"SL: {total_stats['sl']}\n"
        f"OPEN: {total_stats['open']}\n"
        f"Trade chiusi: {total_stats['closed']}\n"
        f"Win Rate totale: {total_stats['win_rate']:.2f}%\n"
        f"Profit Factor: {total_stats['profit_factor']}\n"
        f"Profitto totale: {total_stats['gross_profit']:+.2f} €\n"
        f"Perdita totale: {total_stats['gross_loss']:.2f} €\n"
        f"Profitto teorico totale: {total_stats['net_profit']:+.2f} €\n\n"
        "Operazioni ultime 24 ore\n"
        f"{recent_lines}"
    )


def _stats(trades):
    counts = Counter(trade.get("status", STATUS_OPEN) for trade in trades)
    total = len(trades)
    tp1 = counts[STATUS_TP1]
    sl = counts[STATUS_SL]
    open_count = counts[STATUS_OPEN]
    closed = tp1 + sl
    gross_profit = round(sum(max(float(trade.get("profit_eur", 0.0)), 0.0) for trade in trades), 2)
    gross_loss = round(sum(min(float(trade.get("profit_eur", 0.0)), 0.0) for trade in trades), 2)
    net_profit = round(gross_profit + gross_loss, 2)
    win_rate = (tp1 / closed * 100) if closed else 0.0
    profit_factor = "∞" if gross_loss == 0 and gross_profit > 0 else "0.00"
    if gross_loss < 0:
        profit_factor = f"{gross_profit / abs(gross_loss):.2f}"

    return {
        "total": total,
        "tp1": tp1,
        "sl": sl,
        "open": open_count,
        "closed": closed,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "net_profit": net_profit,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
    }


def _format_recent_trades(trades):
    if not trades:
        return "Nessuna operazione nelle ultime 24 ore."

    lines = []
    for trade in sorted(trades, key=lambda item: item.get("created_at", "")):
        lines.append(
            f"{trade['pair']} {trade['direction']}\n"
            f"Entry {trade['entry']:.6g}\n"
            f"TP1 {trade['target_1']:.6g}\n"
            f"SL {trade['stop_loss']:.6g}\n"
            f"Esito {trade.get('status', STATUS_OPEN)}\n"
            f"Profitto {float(trade.get('profit_eur', 0.0)):+.2f} €"
        )

    return "\n\n".join(lines)


def _created_at(trade):
    value = trade.get("created_at")
    if value:
        parsed = datetime.fromisoformat(value)
        return parsed.astimezone(ROME_TZ)

    return datetime.fromtimestamp(int(trade["candle_time"]), tz=ROME_TZ)

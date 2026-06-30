"""Best-effort recovery of previously generated signals from local log files.

Telegram Bot API does not expose historical messages already sent by a bot. When
local logs are available, this module parses Telegram-style signal messages and
adds missing trades to the persistent archive. If no logs exist, the archive is
left ready for future signals.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from trade_history import TradeHistory
from utils import log

SIGNAL_PATTERN = re.compile(
    r"(?P<direction>LONG|SHORT)\s+(?P<symbol>[A-Z0-9]+)/USD.*?"
    r"Entry:\s*(?P<entry>[0-9.]+).*?"
    r"Stop Loss:\s*(?P<stop>[0-9.]+).*?"
    r"Target 1:\s*(?P<tp1>[0-9.]+).*?"
    r"Target 2:\s*(?P<tp2>[0-9.]+)",
    re.DOTALL,
)


def recover_history(history=None, search_paths=None):
    history = history or TradeHistory()
    recovered = 0

    for path in _candidate_logs(search_paths):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for index, match in enumerate(SIGNAL_PATTERN.finditer(content)):
            signal = _signal_from_match(match, path, index)
            if history.add_signal(signal, ["Recuperato da log locale"]):
                recovered += 1

    if recovered:
        log("HISTORY", f"Recuperati {recovered} segnali da log locali")

    return recovered


def _candidate_logs(search_paths=None):
    roots = [Path(path) for path in (search_paths or [".", "logs", "data"])]
    for root in roots:
        if not root.exists():
            continue
        if root.is_file() and root.suffix.lower() in {".log", ".txt"}:
            yield root
            continue
        for suffix in ("*.log", "*.txt"):
            yield from root.glob(suffix)


def _signal_from_match(match, path, index):
    groups = match.groupdict()
    # Without timestamps in legacy logs, use a stable synthetic timestamp so the
    # import remains idempotent and does not collide with live candle times.
    digest = hashlib.sha256(f"{path}:{index}".encode("utf-8")).hexdigest()
    candle_time = 1_600_000_000 + int(digest[:8], 16) % 100_000_000
    return {
        "symbol": groups["symbol"],
        "direction": groups["direction"],
        "entry": float(groups["entry"]),
        "stop": float(groups["stop"]),
        "tp1": float(groups["tp1"]),
        "tp2": float(groups["tp2"]),
        "timeframe": "5m",
        "candle_time": candle_time,
    }

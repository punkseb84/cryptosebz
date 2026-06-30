"""Daily report scheduler with restart-safe send state."""

from __future__ import annotations

import json
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from config import DAILY_REPORT_STATE_FILE
from daily_report import send_daily_report
from trade_history import TradeHistory
from trade_monitor import monitor_open_trades
from utils import log

ROME_TZ = ZoneInfo("Europe/Rome")
REPORT_TIME = time(9, 0)


class DailyReportScheduler:
    def __init__(self, state_file=DAILY_REPORT_STATE_FILE, history=None):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.history = history or TradeHistory()

    def run_pending(self, now=None):
        now = now or datetime.now(ROME_TZ)
        if now.tzinfo is None:
            now = now.replace(tzinfo=ROME_TZ)

        today = now.date().isoformat()
        if now.time() < REPORT_TIME or self._last_sent_date() == today:
            return False

        monitor_open_trades(self.history)
        send_daily_report(self.history, now=now)
        self._write_state({"last_sent_date": today})
        log("REPORT", f"Report giornaliero inviato per {today}")
        return True

    def _last_sent_date(self):
        try:
            with self.state_file.open("r", encoding="utf-8") as handle:
                return json.load(handle).get("last_sent_date")
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def _write_state(self, state):
        with self.state_file.open("w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)

"""
Crypto Scanner - Entry Point Railway compatible.
"""

import time

from config import SCAN_INTERVAL_SECONDS
from history_recovery import recover_history
from scanner import run_scanner
from scheduler import DailyReportScheduler


def main():
    recover_history()
    scheduler = DailyReportScheduler()

    while True:
        run_scanner()
        scheduler.run_pending()
        time.sleep(SCAN_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

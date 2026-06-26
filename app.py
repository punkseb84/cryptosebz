"""
Crypto Scanner - Entry Point Railway compatible.
"""

import time

from config import SCAN_INTERVAL_SECONDS
from scanner import run_scanner


def main():
    while True:
        run_scanner()
        time.sleep(SCAN_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

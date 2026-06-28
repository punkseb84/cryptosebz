import os

import requests

# ==========================================================
# TELEGRAM
# ==========================================================

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ==========================================================
# KRAKEN
# ==========================================================

KRAKEN_URL = "https://api.kraken.com/0/public/OHLC"
KRAKEN_ASSET_PAIRS_URL = "https://api.kraken.com/0/public/AssetPairs"

TIMEFRAME_MAIN = 5
TIMEFRAME_CONFIRM_15M = 15
TIMEFRAME_CONFIRM_1H = 60
SCAN_INTERVAL_SECONDS = 300

# ==========================================================
# COINS
# ==========================================================

KRAKEN_WATCHLIST_SIZE = 16

KRAKEN_CANDIDATE_SYMBOLS = [
    "BTC",
    "ETH",
    "SOL",
    "XRP",
    "BNB",
    "DOGE",
    "ADA",
    "TRX",
    "LINK",
    "AVAX",
    "SUI",
    "HYPE",
    "BCH",
    "LTC",
    "XLM",
    "TON",
    "DOT",
    "SHIB",
    "HBAR",
    "UNI",
    "PEPE",
]

KRAKEN_PAIR_FALLBACKS = {
    "BTC": "XBTUSD",
    "ETH": "ETHUSD",
    "SOL": "SOLUSD",
    "XRP": "XRPUSD",
    "BNB": "BNBUSD",
    "DOGE": "DOGEUSD",
    "ADA": "ADAUSD",
    "TRX": "TRXUSD",
    "LINK": "LINKUSD",
    "AVAX": "AVAXUSD",
    "SUI": "SUIUSD",
    "HYPE": "HYPEUSD",
    "BCH": "BCHUSD",
    "LTC": "LTCUSD",
    "XLM": "XLMUSD",
    "TON": "TONUSD",
    "DOT": "DOTUSD",
    "SHIB": "SHIBUSD",
    "HBAR": "HBARUSD",
    "UNI": "UNIUSD",
    "PEPE": "PEPEUSD",
}


def _symbol_aliases(symbol):
    aliases = {symbol}

    if symbol == "BTC":
        aliases.add("XBT")

    return aliases


def _find_kraken_usd_pair(symbol, asset_pairs):
    aliases = _symbol_aliases(symbol)

    for pair_name, pair_data in asset_pairs.items():
        altname = pair_data.get("altname", "")
        wsname = pair_data.get("wsname", "")

        for alias in aliases:
            if altname == f"{alias}USD" or wsname == f"{alias}/USD":
                return altname or pair_name

    return None


def _load_kraken_asset_pairs():
    response = requests.get(KRAKEN_ASSET_PAIRS_URL, timeout=20)
    response.raise_for_status()
    data = response.json()

    if data.get("error"):
        raise Exception(f"Kraken API Error: {data['error']}")

    return data.get("result", {})


def _resolve_kraken_pairs(symbols, limit=KRAKEN_WATCHLIST_SIZE):
    try:
        asset_pairs = _load_kraken_asset_pairs()
    except Exception:
        return {
            symbol: KRAKEN_PAIR_FALLBACKS[symbol]
            for symbol in symbols[:limit]
            if symbol in KRAKEN_PAIR_FALLBACKS
        }

    resolved = {}

    for symbol in symbols:
        pair = _find_kraken_usd_pair(symbol, asset_pairs)

        if pair is None:
            continue

        resolved[symbol] = pair

        if len(resolved) == limit:
            break

    return resolved


COINS = _resolve_kraken_pairs(KRAKEN_CANDIDATE_SYMBOLS)

# ==========================================================
# INDICATORI / STRATEGIA
# ==========================================================

EMA_FAST = 20
EMA_MID = 50
EMA_SLOW = 200
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ATR_PERIOD = 14
VOLUME_PERIOD = 20
MIN_VOLUME_RATIO = 0.8
SUPPORT_RESISTANCE_PERIOD = 20
NEAR_LEVEL_PERCENT = 0.35

LONG_RSI_MIN = 48
LONG_RSI_MAX = 72
SHORT_RSI_MIN = 28
SHORT_RSI_MAX = 52

ATR_STOP_MULTIPLIER = 1.2
TP1_RR = 1.5
TP2_RR = 2.5

DEBUG = True

# ==========================================================
# COMPATIBILITÀ MODULI LEGACY
# ==========================================================

INTERVAL = TIMEFRAME_MAIN
RVOL_PERIOD = VOLUME_PERIOD
RVOL_MIN = MIN_VOLUME_RATIO
RVOL_CAP = 5.0
WATCHLIST_DISTANCE = 3.0
PRELONG_DISTANCE = 1.5
MIN_RESISTANCE_DISTANCE = 1.0
SUPPORT_DISTANCE = 0.005
BREAKOUT_BUFFER = 0.005
TREND_WEIGHT = 60
RVOL_WEIGHT = 15
DISTANCE_WEIGHT = 10
MAX_WATCHLIST = 5
MAX_PRELONG = 5
MAX_LONG = 5
MIN_LONG_TREND_SCORE = 2
MIN_BREAKOUT_CLOSE_ABOVE_RESISTANCE = 0.0025
MIN_BREAKOUT_BODY_PERCENT = 0.25
MAX_SIGNAL_RISK_PERCENT = 6.0
MIN_SIGNAL_RISK_PERCENT = 0.25
MAX_RESISTANCE_EXTENSION_PERCENT = 12.0

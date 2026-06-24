import os

# ==========================================================
# TELEGRAM
# ==========================================================

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ==========================================================
# KRAKEN
# ==========================================================

KRAKEN_URL = "https://api.kraken.com/0/public/OHLC"
INTERVAL = 240

# ==========================================================
# EMA
# ==========================================================

EMA_FAST = 20
EMA_MID = 50
EMA_SLOW = 200

# ==========================================================
# VOLUME
# ==========================================================

RVOL_PERIOD = 20
RVOL_MIN = 1.20

# ==========================================================
# DISTANZE
# ==========================================================

WATCHLIST_DISTANCE = 3.0
PRELONG_DISTANCE = 2.0

BREAKOUT_BUFFER = 0.005

# ==========================================================
# SCORE
# ==========================================================

TREND_WEIGHT = 100
RVOL_WEIGHT = 10
DISTANCE_WEIGHT = 5

# ==========================================================
# CLASSIFICHE
# ==========================================================

MAX_WATCHLIST = 5
MAX_PRELONG = 5

# ==========================================================
# COINS
# ==========================================================

COINS = {

    "BTC": "XBTUSD",
    "ETH": "ETHUSD",
    "SOL": "SOLUSD",
    "XRP": "XRPUSD",
    "ADA": "ADAUSD",
    "DOGE": "DOGEUSD",
    "LINK": "LINKUSD",
    "AVAX": "AVAXUSD",
    "DOT": "DOTUSD",
    "LTC": "LTCUSD",
    "ATOM": "ATOMUSD",
    "UNI": "UNIUSD",
    "AAVE": "AAVEUSD",
    "FIL": "FILUSD",
    "ALGO": "ALGOUSD",
    "ICP": "ICPUSD",
    "APT": "APTUSD",
    "ARB": "ARBUSD",
    "OP": "OPUSD",
    "NEAR": "NEARUSD",
    "INJ": "INJUSD",
    "SUI": "SUIUSD",
    "SEI": "SEIUSD",
    "TIA": "TIAUSD",
    "JUP": "JUPUSD",
    "SHIB": "SHIBUSD",
    "PEPE": "PEPEUSD",
    "ETC": "ETCUSD",
    "BCH": "BCHUSD"

}
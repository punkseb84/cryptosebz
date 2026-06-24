import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

ticker = requests.get(
    "https://api.exchange.coinbase.com/products/BTC-USD/ticker"
).json()

price = ticker["price"]

message = f"""
📈 BTC/USD

Prezzo attuale:
{price}

Scanner online ✅
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.json())

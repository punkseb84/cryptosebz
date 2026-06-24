import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = """
🚀 Crypto Scanner Online

Primo test riuscito.

Se ricevi questo messaggio significa che:

✅ Railway funziona
✅ Telegram funziona
✅ Variabili ambiente funzionano
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

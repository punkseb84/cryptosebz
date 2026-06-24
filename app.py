import requests

url = "https://api.exchange.coinbase.com/products/BTC-USD/candles"

params = {
    "granularity": 14400  # 4 ore
}

response = requests.get(url, params=params)

data = response.json()

print(f"Candele ricevute: {len(data)}")

print(data[:3])

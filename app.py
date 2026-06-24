import requests

url = "https://api.exchange.coinbase.com/products/BTC-USD/candles"

params = {
    "granularity": 21600
}

response = requests.get(url, params=params)

print("STATUS:", response.status_code)

data = response.json()

print(type(data))
print(data[:3] if isinstance(data, list) else data)

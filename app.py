import requests

url = "https://api.exchange.coinbase.com/products/BTC-USD/candles"

params = {
    "granularity": 14400
}

response = requests.get(url, params=params)

print("STATUS:", response.status_code)
print("RISPOSTA:")
print(response.json())

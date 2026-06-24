import requests

url = "https://api.binance.com/api/v3/ticker/price"

response = requests.get(
    url,
    params={"symbol": "BTCUSDT"}
)

data = response.json()

print("BTC PRICE")
print(data)

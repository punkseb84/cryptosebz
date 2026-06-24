import requests

url = "https://api.exchange.coinbase.com/products/BTC-USD/ticker"

response = requests.get(url)

print(response.json())

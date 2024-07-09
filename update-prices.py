import requests
import json

url = "https://price.api.cx.metamask.io/v1/exchange-rates?baseCurrency=usd"
response = requests.get(url)
data = response.json()

prices = {
    "btc": data["btc"]["value"],
    "eth": data["eth"]["value"],
    "ltc": data["ltc"]["value"]
}

with open("README.md", "r") as file:
    readme = file.readlines()

for i, line in enumerate(readme):
    if line.startswith("![Bitcoin Price]"):
        readme[i] = f"![Bitcoin Price](https://img.shields.io/badge/Bitcoin-{prices['btc']}-btc.svg?style=flat-square)\n"
    elif line.startswith("![Ethereum Price]"):
        readme[i] = f"![Ethereum Price](https://img.shields.io/badge/Ethereum-{prices['eth']}-eth.svg?style=flat-square)\n"
    elif line.startswith("![Litecoin Price]"):
        readme[i] = f"![Litecoin Price](https://img.shields.io/badge/Litecoin-{prices['ltc']}-ltc.svg?style=flat-square)\n"

with open("README.md", "w") as file:
    file.writelines(readme)

import requests
import json

# Fetch cryptocurrency prices
price_url = "https://price.api.cx.metamask.io/v1/exchange-rates?baseCurrency=usd"
price_response = requests.get(price_url)
price_data = price_response.json()

# Fetch donation balances
donation_url = "https://accounts.api.cx.metamask.io/v2/accounts/0x3a06322e9f1124f6b2de8f343d4fdce4d1009869/balances?networks=1%2C10%2C56%2C137%2C8453%2C59144&includeUnverifiedAssets=true&filterSupportedTokens=true"
donation_response = requests.get(donation_url)
donation_data = donation_response.json()

# Create README.md content
readme_content = f"""# Cryptocurrency Prices

![Bitcoin Price](https://img.shields.io/badge/Bitcoin-{price_data['btc']['value']}-btc.svg?style=flat-square)
![Ethereum Price](https://img.shields.io/badge/Ethereum-{price_data['eth']['value']}-eth.svg?style=flat-square)
![Litecoin Price](https://img.shields.io/badge/Litecoin-{price_data['ltc']['value']}-ltc.svg?style=flat-square)

# Donation Trackers

![ETH Donations](https://img.shields.io/badge/ETH-{donation_data['balances'][1]['balance']}-eth.svg?style=flat-square)
![BNB Donations](https://img.shields.io/badge/BNB-{donation_data['balances'][6]['balance']}-bnb.svg?style=flat-square)

# Live Updates from Telegram

<div class="telegram-post-widget" data-telegram-post="Telegram/5"></div>
<script async src="https://telegram.org/js/telegram-widget.js?14" data-telegram-post="Telegram/5"></script>
"""

# Save to README.md file
with open("README.md", "w") as file:
    file.write(readme_content)

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Fetch cryptocurrency prices
price_url = "https://price.api.cx.metamask.io/v1/exchange-rates?baseCurrency=usd"
price_response = requests.get(price_url)
price_data = price_response.json()

# Fetch donation balances
donation_url = "https://accounts.api.cx.metamask.io/v2/accounts/0x3a06322e9f1124f6b2de8f343d4fdce4d1009869/balances?networks=1%2C10%2C56%2C137%2C8453%2C59144&includeUnverifiedAssets=true&filterSupportedTokens=true"
donation_response = requests.get(donation_url)
donation_data = donation_response.json()

# Generate cryptocurrency price images
def generate_price_image(ticker, value):
    image = Image.new('RGB', (200, 60), color = (73, 109, 137))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), f"{ticker}: {value:.8f}", font=font, fill=(255, 255, 255))
    image.save(f"{ticker}.png")

generate_price_image("BTC", price_data['btc']['value'])
generate_price_image("ETH", price_data['eth']['value'])
generate_price_image("LTC", price_data['ltc']['value'])

# Generate donation balance images
def generate_donation_image(symbol, balance):
    image = Image.new('RGB', (300, 60), color = (73, 109, 137))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), f"{symbol} Donations: {balance}", font=font, fill=(255, 255, 255))
    image.save(f"{symbol}_donations.png")

generate_donation_image("ETH", donation_data['balances'][1]['balance'])
generate_donation_image("BNB", donation_data['balances'][6]['balance'])

# Generate GIF for cryptocurrency prices
def generate_price_gif(price_data):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 100)
    ax.set_title('Cryptocurrency Prices')
    
    bars = ax.bar(['BTC', 'ETH', 'LTC'], [price_data['btc']['value'] * 1000, price_data['eth']['value'] * 1000, price_data['ltc']['value'] * 1000])
    
    def animate(i):
        for bar, value in zip(bars, [price_data['btc']['value'] * 1000, price_data['eth']['value'] * 1000, price_data['ltc']['value'] * 1000]):
            bar.set_height(value + i)
    
    ani = animation.FuncAnimation(fig, animate, frames=10, repeat=False)
    ani.save('crypto_prices.gif', writer='imagemagick')

generate_price_gif(price_data)

# Fetch transactions
transaction_url_eth = "https://account.api.cx.metamask.io/networks/1/accounts/0x3a06322e9f1124f6b2de8f343d4fdce4d1009869/transactions"
transaction_response_eth = requests.get(transaction_url_eth)
transactions_eth = transaction_response_eth.json()['data']

transaction_url_bsc = "https://account.api.cx.metamask.io/networks/56/accounts/0x3a06322e9f1124f6b2de8f343d4fdce4d1009869/transactions"
transaction_response_bsc = requests.get(transaction_url_bsc)
transactions_bsc = transaction_response_bsc.json()['data']

# Generate stylish graph for transactions
def generate_transaction_graph(transactions_eth, transactions_bsc):
    eth_values = [tx['valueDisplay'] for tx in transactions_eth[:10]]
    bsc_values = [tx['valueDisplay'] for tx in transactions_bsc[:10]]
    
    fig, ax = plt.subplots()
    ax.plot(range(len(eth_values)), eth_values, label='ETH', color='b')
    ax.plot(range(len(bsc_values)), bsc_values, label='BSC', color='g')
    
    ax.set_xlabel('Transaction Index')
    ax.set_ylabel('Value')
    ax.set_title('Recent Transactions')
    ax.legend()
    
    plt.savefig('transactions_graph.png')

generate_transaction_graph(transactions_eth, transactions_bsc)

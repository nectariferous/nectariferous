import requests
import json
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Fetch cryptocurrency prices
price_url = "https://price.api.cx.metamask.io/v1/exchange-rates?baseCurrency=usd"
price_response = requests.get(price_url)
price_data = price_response.json()

# Fetch donation balances
donation_url = "https://accounts.api.cx.metamask.io/v2/accounts/0x3a06322e9f1124f6b2de8f343d4fdce4d1009869/balances?networks=1%2C10%2C56%2C137%2C8453%2C59144&includeUnverifiedAssets=true&filterSupportedTokens=true"
donation_response = requests.get(donation_url)
donation_data = donation_response.json()

# Function to delete existing image if exists
def delete_existing_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)

# Load font
def load_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()

# Generate gradient background
def create_gradient_background(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (1 - y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

# Add rounded corners to image
def add_rounded_corners(image, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    alpha = Image.new('L', image.size, 255)
    w, h = image.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    image.putalpha(alpha)
    return image

# Generate cryptocurrency price images
def generate_price_image(ticker, value):
    delete_existing_file(f"{ticker}.png")
    image = create_gradient_background(200, 60, (0, 0, 0), (0, 100, 0))
    draw = ImageDraw.Draw(image)
    font = load_font(24)
    draw.text((10, 10), f"{ticker}: {value}", font=font, fill=(0, 255, 0))
    image = add_rounded_corners(image, 15)
    image.save(f"{ticker}.png")

generate_price_image("BTC", price_data['btc']['value'])
generate_price_image("ETH", price_data['eth']['value'])
generate_price_image("LTC", price_data['ltc']['value'])

# Generate donation balance images
def generate_donation_image(symbol, balance):
    delete_existing_file(f"{symbol}_donations.png")
    image = create_gradient_background(300, 60, (0, 0, 0), (100, 0, 0))
    draw = ImageDraw.Draw(image)
    font = load_font(24)
    draw.text((10, 10), f"{symbol} Donations: {balance}", font=font, fill=(255, 0, 0))
    image = add_rounded_corners(image, 15)
    image.save(f"{symbol}_donations.png")

generate_donation_image("ETH", donation_data['balances'][1]['balance'])
generate_donation_image("BNB", donation_data['balances'][6]['balance'])

# Generate GIF for cryptocurrency prices
def generate_price_gif(price_data):
    delete_existing_file('crypto_prices.gif')
    
    fig, ax = plt.subplots(facecolor='black')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 100000)
    ax.set_title('Cryptocurrency Prices', color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    bars = ax.bar(['BTC', 'ETH', 'LTC'], [price_data['btc']['value'] * 1000, price_data['eth']['value'] * 1000, price_data['ltc']['value'] * 1000], color=['green', 'red', 'blue'])
    
    def animate(i):
        for bar, value in zip(bars, [price_data['btc']['value'] * 1000, price_data['eth']['value'] * 1000, price_data['ltc']['value'] * 1000]):
            bar.set_height(value + i * 100)
    
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
    delete_existing_file('transactions_graph.png')
    
    eth_values = [float(tx['valueDisplay'].replace(',', '')) for tx in transactions_eth[:10]]
    bsc_values = [float(tx['valueDisplay'].replace(',', '')) for tx in transactions_bsc[:10]]
    
    fig, ax = plt.subplots(facecolor='black')
    ax.plot(range(len(eth_values)), eth_values, label='ETH', color='lime')
    ax.plot(range(len(bsc_values)), bsc_values, label='BSC', color='red')
    
    ax.set_xlabel('Transaction Index', color='white')
    ax.set_ylabel('Value', color='white')
    ax.set_title('Recent Transactions', color='white')
    ax.legend()
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.savefig('transactions_graph.png', facecolor='black')

generate_transaction_graph(transactions_eth, transactions_bsc)

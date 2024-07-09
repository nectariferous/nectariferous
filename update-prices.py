import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import patheffects
import seaborn as sns
import numpy as np
import io
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from moviepy.editor import ImageSequenceClip
import plotly.graph_objects as go

# Fetch cryptocurrency prices
price_url = "https://price.api.cx.metamask.io/v1/exchange-rates?baseCurrency=usd"
price_response = requests.get(price_url)
price_data = price_response.json()

# Fetch donation balances (Replace with your MetaMask account)
donation_url = "https://accounts.api.cx.metamask.io/v2/accounts/<YOUR_METAMASK_ACCOUNT>/balances?networks=1%2C10%2C56%2C137%2C8453%2C59144&includeUnverifiedAssets=true&filterSupportedTokens=true"
donation_response = requests.get(donation_url)
donation_data = donation_response.json()

# Fetch transactions (Replace with your MetaMask account)
transaction_url_eth = "https://account.api.cx.metamask.io/networks/1/accounts/<YOUR_METAMASK_ACCOUNT>/transactions"
transaction_response_eth = requests.get(transaction_url_eth)
transactions_eth = transaction_response_eth.json()['data']

transaction_url_bsc = "https://account.api.cx.metamask.io/networks/56/accounts/<YOUR_METAMASK_ACCOUNT>/transactions"
transaction_response_bsc = requests.get(transaction_url_bsc)
transactions_bsc = transaction_response_bsc.json()['data']

# Ultra-Stylish Price Image Generation
def generate_price_image(ticker, value, color, sparkline_data):
    image = Image.new('RGBA', (500, 200), color=(26, 35, 126, 0)) 
    draw = ImageDraw.Draw(image)

    # Futuristic Fonts
    title_font = ImageFont.truetype("NovaMono.ttf", 60)  
    value_font = ImageFont.truetype("NovaMono.ttf", 48)

    # Gradient Background
    for y in range(200):
        r, g, b = color
        r += int(y * 0.5)  
        g += int(y * 0.5)
        b += int(y * 0.5)
        draw.line((0, y, 500, y), fill=(r, g, b), width=1)

    # Text with Outline
    draw.text((30, 30), f"{ticker}", font=title_font, fill="white", stroke_width=3, stroke_fill="black")
    draw.text((30, 90), f"${value:.2f}", font=value_font, fill="white")

    # Sparkline with Gradient Fill
    fig = plt.figure(figsize=(2.5, 0.8), dpi=100)
    ax = fig.add_subplot(111, facecolor='none') 
    ax.plot(sparkline_data, color='white', linewidth=2)
    ax.fill_between(range(len(sparkline_data)), sparkline_data, color=color, alpha=0.5)
    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    sparkline_img = Image.open(buf)
    image.paste(sparkline_img, (350, 80))

    image.save(f"{ticker}_price_ultra.png")

# Enhanced Donation Image Generation (with background image and glowing effect)
def generate_donation_image(symbol, balance, image_path="background.png"):
    background = Image.open(image_path)
    background = background.resize((500, 200))

    donation_image = Image.new("RGBA", background.size)
    donation_image = Image.alpha_composite(donation_image, background)

    draw = ImageDraw.Draw(donation_image)

    # Stylish Fonts with Glow Effect
    title_font = ImageFont.truetype("NovaMono.ttf", 50)
    glow_radius = 10

    # Create glow effect by drawing multiple layers of blurred text
    for offset in range(-glow_radius, glow_radius + 1):
        for x_offset, y_offset in [(offset, 0), (0, offset), (offset, offset), (-offset, offset)]:
            draw.text((30 + x_offset, 80 + y_offset), f"{symbol} Donations:", font=title_font, fill=(255, 255, 255, 128))

    draw.text((30, 80), f"{symbol} Donations:", font=title_font, fill="white")  # Main text
    draw.text((30, 130), f"{balance}", font=title_font, fill="white")

    donation_image.save(f"{symbol}_donation_ultra.png")


# 3D Transaction Graph with Animation
def generate_3d_transaction_graph(transactions_eth, transactions_bsc):
    eth_values = [tx['valueDisplay'] for tx in transactions_eth[:10]]
    bsc_values = [tx['valueDisplay'] for tx in transactions_bsc[:10]]

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=range(len(eth_values)), 
                              y=[1] * len(eth_values),  # ETH on y-axis = 1
                              z=eth_values,
                              mode='lines+markers',
                              name='ETH',
                              line=dict(color='#3498db'),  # Ethereum blue
                              marker=dict(size=8, color='#3498db')))
    
    fig.add_trace(go.Scatter3d(x=range(len(bsc_values)), 
                              y=[2] * len(bsc_values),  # BSC on y-axis = 2
                              z=bsc_values,
                              mode='lines+markers',
                              name='BSC',
                              line=dict(color='#f1c40f'),  # Binance yellow
                              marker=dict(size=8, color='#f1c40f')))

    fig.update_layout(
        scene=dict(
            xaxis_title='Transaction Index',
            yaxis_title='Network',
            zaxis_title='Value',
            xaxis=dict(tickmode='linear'),  # Force linear ticks for clarity
            yaxis=dict(tickvals=[1, 2], ticktext=['ETH', 'BSC']),  # Label y-axis 
            bgcolor='rgba(0,0,0,0.8)'  # Darker background
        ),
        margin=dict(l=0, r=0, b=0, t=0),  # Remove margins
        paper_bgcolor='rgba(0,0,0,0)'  # Transparent paper background
    )

    # Animation
    frames = []
    for i in range(1, len(eth_values) + 1):
        frame = go.Frame(
            data=[
                go.Scatter3d(x=range(i), y=[1] * i, z=eth_values[:i]),
                go.Scatter3d(x=range(i), y=[2] * i, z=bsc_values[:i])
            ]
        )
        frames.append(frame)
    
    fig.frames = frames
    fig.update_layout(updatemenus=[dict(type="buttons",
                                    showactive=False,
                                    buttons=[dict(label="Play",
                                                  method="animate",
                                                  args=[None])])])

    fig.show()



# Animated Price GIF (Improved)
def generate_animated_price_gif(price_data, frames=20):
    colors = {'BTC': '#f2a900', 'ETH': '#627eea', 'LTC': '#bfbbbb'}  

    image_frames = []
    for i in range(frames):
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='black') 
        ax.set_facecolor('black')  

        for ticker, value in price_data.items():
            sparkline_data = np.random.randn(10) + value['value']  
            generate_price_image(ticker, value['value'], colors[ticker], sparkline_data)
            img = plt.imread(f"{ticker}_price_ultra.png")

            # Smooth animation of image positions
            x_pos = 0.5 + 0.05 * np.sin(2 * np.pi * i / frames)  # Subtle horizontal oscillation
            y_pos = value['value'] / 50 + 0.02 * np.cos(2 * np.pi * i / frames) # Subtle vertical oscillation

            imagebox = OffsetImage(img, zoom=0.5)
            ab = AnnotationBbox(imagebox, (x_pos, y_pos), frameon=False, xycoords='data', boxcoords="offset points", pad=0)
            ax.add_artist(ab)

        ax.axis('off')
        fig.canvas.draw()
        image = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        image_frames.append(image)
        plt.close(fig)

    clip = ImageSequenceClip(image_frames, fps=10)
    clip.write_gif("animated_prices_smooth.gif")
    

# Call the functions to create visualizations
generate_3d_transaction_graph(transactions_eth, transactions_bsc)
generate_animated_price_gif(price_data)

# Call the Functions
generate_animated_price_gif(price_data)

# Examples
generate_price_image("BTC", price_data['btc']['value'], (255, 165, 0), np.random.randn(10) + price_data['btc']['value'])
generate_price_image("ETH", price_data['eth']['value'], (100, 149, 237), np.random.randn(10) + price_data['eth']['value'])
generate_price_image("LTC", price_data['ltc']['value'], (192, 192, 192), np.random.randn(10) + price_data['ltc']['value'])


generate_donation_image("ETH", donation_data['balances'][1]['balance'])  
generate_donation_image("BNB", donation_data['balances'][6]['balance']) 

generate_3d_transaction_graph(transactions_eth, transactions_bsc)

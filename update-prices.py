import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Fetch cryptocurrency prices
def fetch_crypto_prices():
    price_url = "https://price.api.cx.metamask.io/v1/exchange-rates?baseCurrency=usd"
    try:
        price_response = requests.get(price_url)
        price_response.raise_for_status()  # Raises an HTTPError for bad responses
        return price_response.json()
    except requests.RequestException as e:
        print(f"Error fetching prices: {e}")
        return None

# Fetch cryptocurrency account balances
def fetch_crypto_balances(account):
    donation_url = f"https://accounts.api.cx.metamask.io/v2/accounts/{account}/balances?networks=1%2C10%2C56%2C137%2C8453%2C59144&includeUnverifiedAssets=true&filterSupportedTokens=true"
    try:
        donation_response = requests.get(donation_url)
        donation_response.raise_for_status()
        return donation_response.json()
    except requests.RequestException as e:
        print(f"Error fetching balances: {e}")
        return None

# Generate a gradient background
def generate_gradient_background(width, height, top_color, bottom_color):
    background = Image.new('RGB', (width, height), "black")
    draw = ImageDraw.Draw(background)
    for i in range(height):
        r = top_color[0] + (bottom_color[0] - top_color[0]) * i / height
        g = top_color[1] + (bottom_color[1] - top_color[1]) * i / height
        b = top_color[2] + (bottom_color[2] - top_color[2]) * i / height
        draw.line([(0, i), (width, i)], fill=(int(r), int(g), int(b)))
    return background

# Apply text effects for glow and shadow
def apply_text_effects(draw, text, position, font, glow_color, shadow_color):
    x, y = position
    glow_radius = 10
    # Shadow
    draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
    # Glow
    for offset in range(-glow_radius, glow_radius + 1):
        draw.text((x + offset, y + offset), text, font=font, fill=glow_color)

# Generate an advanced donation image
def generate_donation_image(symbol, balance):
    width, height = 500, 200
    top_color = (0, 156, 215)  # Light blue top
    bottom_color = (0, 31, 63)  # Dark blue bottom

    background = generate_gradient_background(width, height, top_color, bottom_color)
    donation_image = Image.new("RGBA", (width, height))
    donation_image.paste(background)

    font = ImageFont.truetype("arial.ttf", 50)
    text = f"{symbol} Donations: {balance}"
    position = (30, 80)
    glow_color = (255, 255, 255, 150)
    shadow_color = (0, 0, 0, 180)

    draw = ImageDraw.Draw(donation_image)
    apply_text_effects(draw, text, position, font, glow_color, shadow_color)
    draw.text(position, text, font=font, fill="white")

    donation_image.save(f"{symbol}_donation_ultra.png")

# Main function to orchestrate calls
def main():
    # Replace '<YOUR_METAMASK_ACCOUNT>' with your actual MetaMask account ID
    account_id = "0x3A06322e9F1124F6B2de8F343D4FDce4D1009869"
    crypto_data = fetch_crypto_prices()
    balances_data = fetch_crypto_balances(account_id)
    
    if crypto_data and balances_data:
        # Generate images for BTC, ETH, LTC or other cryptocurrencies listed in your balance
        for balance in balances_data.get('balances', []):
            symbol = balance.get('asset_symbol', 'UNKNOWN')
            amount = balance.get('balance', '0')
            generate_donation_image(symbol, amount)
    else:
        print("Failed to fetch data or generate images")

if __name__ == "__main__":
    main()

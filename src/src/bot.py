import json
from binance.client import Client
from indicators import calculate_indicators
from notifier import send_alert

# Load configuration
with open('../config/config.json') as f:
    config = json.load(f)

with open('../config/secrets.json') as f:
    secrets = json.load(f)

# Initialize Binance client
client = Client(secrets['binance_api_key'], secrets['binance_api_secret'])

def check_signals():
    for pair in config['pairs']:
        # Get recent candle data
        candles = client.get_klines(
            symbol=pair,
            interval=config['timeframe'],
            limit=100
        )
        
        # Extract closing prices
        closes = [float(candle[4]) for candle in candles]
        
        # Calculate indicators
        signals = calculate_indicators(closes)
        
        # Check buy/sell conditions
        if signals['buy_signal']:
            send_alert(f"BUY {pair} at {closes[-1]}")
        elif signals['sell_signal']:
            send_alert(f"SELL {pair} at {closes[-1]}")

if __name__ == "__main__":
    check_signals()

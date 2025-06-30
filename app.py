from flask import Flask
import os
import threading
import time
import requests

app = Flask(__name__)

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = '8198543545:AAHe3bpRApOvX-CqFT4oWB-DdLFaeq4nc6U'
TELEGRAM_CHAT_ID = '7111651983'

# Coins to monitor
COINS = [
    "ADAUSDT",
    "HBARUSDT",
    "ENAUSDT",
    "SUIUSDT",
    "COTIUSDT"
]

# Binance API endpoint
BINANCE_API = "https://api.binance.com/api/v3/klines"

# Send Telegram alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

# Fetch 1-minute candlesticks (16 minutes worth)
def get_ohlcv(symbol):
    params = {
        "symbol": symbol,
        "interval": "1m",
        "limit": 16
    }
    try:
        response = requests.get(BINANCE_API, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

# Analyze for price/volume changes
def analyze_market():
    while True:
        for coin in COINS:
            data = get_ohlcv(coin)
            if data and len(data) >= 16:
                old_price = float(data[0][4])
                new_price = float(data[-1][4])
                old_volume = float(data[0][5])
                new_volume = sum(float(x[5]) for x in data[-15:])

                price_change = ((new_price - old_price) / old_price) * 100
                volume_change = ((new_volume - old_volume) / old_volume) * 100 if old_volume > 0 else 0

                if abs(price_change) >= 2:
                    send_telegram_alert(
                        f"📈 {coin} price changed {price_change:.2f}% in 15 min.\nOld: {old_price}, New: {new_price}"
                    )

                if abs(volume_change) >= 30:
                    send_telegram_alert(
                        f"📊 {coin} volume changed {volume_change:.2f}% in 15 min.\nVolume: {new_volume:.2f}"
                    )
        time.sleep(60)

@app.route('/')
def home():
    return '✅ Crypto Alert Bot is Running on Render!'

# Test Telegram alert on startup
send_telegram_alert("✅ Test alert: Your crypto bot has

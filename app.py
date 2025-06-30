from flask import Flask
import os
import threading
import time
import requests

app = Flask(__name__)

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = '8198543545:AAHe3bpRApOvX-CqFT4oWB-DdLFaeq4nc6U'
TELEGRAM_CHAT_ID = '7111651983'

# Coins to track
COINS = ['ADAUSDT', 'HBARUSDT', 'ENAUSDT', 'SUIUSDT', 'COTIUSDT']

# Binance Kline API
BINANCE_API = "https://api.binance.com/api/v3/klines"

# Send message to Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

# Get last 16 minutes of candlestick data
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

# Analyze market and send alerts
def analyze_market():
    while True:
        for coin in COINS:
            data = get_ohlcv(coin)
            if data and len(data) >= 16:
                old_price = float(data[0][4])
                new_price = float(data[-1][4])
                old_volume = float(data[0][5])
                new_volume = sum(float(x[5]) for x in data[-15:

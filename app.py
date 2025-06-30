from flask import Flask
import os
import threading
import time
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Telegram Bot Info
TELEGRAM_BOT_TOKEN = '8198543545:AAHe3bpRApOvX-CqFT4oWB-DdLFaeq4nc6U'
TELEGRAM_CHAT_ID = '7111651983'

# Coins to monitor
COINS = ['ADAUSDT', 'HBARUSDT', 'ENAUSDT', 'SUIUSDT', 'COTIUSDT']

# Binance API endpoint
BINANCE_API = "https://api.binance.com/api/v3/klines"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram error: {e}")

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

def analyze_market():
    while True:
        for coin in COINS:
            data = get_ohlcv(coin)
            if data and len(data) >= 16:
                old_price = float(data[0][4])
                new_price = float(data[-1][4])
                old_volume = sum(float(x[5]) for x in data[:1])
                new_volume = sum(float(x[5]) for x in data[-15:])

                price_change = ((new_price - old_price) / old_price) * 100
                volume_change = ((new_volume - old_volume) / old_volume) * 100 if old_volume > 0 else 0

                if abs(price_change) >= 2:
                    msg = f"📈 {coin} price changed {price_change:.2f}% in 15 minutes.\nOld: {old_price}, New: {new_price}"
                    send_telegram_alert(msg)

                if abs(volume_change) >= 30:
                    msg = f"📊 {coin} volume changed {volume_change:.2f}% in 15 minutes.\nVolume: {new_volume:.2f}"
                    send_telegram_alert(msg)

        time.sleep(60)

@app.route('/')
def home():
    return '✅ Crypto Alert System is Running!'

# Start background thread
threading.Thread(target=analyze_market, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

import time
import requests
from datetime import datetime, timedelta

TELEGRAM_BOT_TOKEN = '8198543545:AAHe3bpRApOvX-CqFT4oWB-DdLFaeq4nc6U'
TELEGRAM_CHAT_ID = '7111651983'

SYMBOLS = ['ADAUSDT', 'HBARUSDT', 'ENAUSDT', 'SUIUSDT', 'COTIUSDT', 'XRPUSDT', 'THETAUSDT']
PRICE_THRESHOLD = 0.5
VOLUME_THRESHOLD = 10
INTERVAL = '1m'
WINDOW_MINUTES = 15

def send_telegram_alert(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def get_klines(symbol, interval, limit):
    url = f'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    response = requests.get(url, params=params)
    return response.json()

def analyze_market():
    for symbol in SYMBOLS:
        try:
            klines = get_klines(symbol, interval=INTERVAL, limit=WINDOW_MINUTES)
            if len(klines) < WINDOW_MINUTES:
                continue

            open_price = float(klines[0][1])
            close_price = float(klines[-1][4])
            volume_start = float(klines[0][5])
            volume_end = float(klines[-1][5])

            price_change = ((close_price - open_price) / open_price) * 100
            volume_change = ((volume_end - volume_start) / volume_start) * 100 if volume_start else 0

            if abs(price_change) >= PRICE_THRESHOLD or abs(volume_change) >= VOLUME_THRESHOLD:
                direction = "🚀 Pump" if price_change > 0 else "📉 Dump"
                alert = (
                    f"{direction} detected for {symbol}:\n"
                    f"Price change: {price_change:.2f}%\n"
                    f"Volume change: {volume_change:.2f}%\n"
                    f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
                )
                send_telegram_alert(alert)

        except Exception as e:
            print(f"Error with {symbol}: {e}")

if __name__ == '__main__':
    send_telegram_alert("🚨 Test Alert: Your Render-based Crypto Alert System is now running.")
    while True:
        analyze_market()
        time.sleep(60)

import requests
from datetime import datetime
from senders import send_alert  # Replace with your alert function location

symbols = [
    "SUIUSDT", "XLMUSDT", "HBARUSDT",
    "ADAUSDT", "ENAUSDT", "COTIUSDT",
    "THETAUSDT", "VETUSDT", "XRPUSDT"
]

def get_klines(symbol):
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": "1m", "limit": 15}
    response = requests.get(url, params=params)
    return response.json()

def check_market():
    for symbol in symbols:
        try:
            klines = get_klines(symbol)

            high_prices = [float(k[2]) for k in klines]
            low_prices = [float(k[3]) for k in klines]
            volumes = [float(k[5]) for k in klines]

            min_price = min(low_prices)
            max_price = max(high_prices)
            price_change_percent = ((max_price - min_price) / min_price) * 100

            start_volume = volumes[0]
            end_volume = volumes[-1]
            volume_change_percent = ((end_volume - start_volume) / start_volume) * 100 if start_volume > 0 else 0

            print(f"[{datetime.now()}] {symbol}:")
            print(f"  Price Change: {price_change_percent:.2f}% (High: {max_price}, Low: {min_price})")
            print(f"  Volume Change: {volume_change_percent:.2f}%")

            if price_change_percent >= 2:
                send_alert(f"🚀 {symbol} is pumping! +{price_change_percent:.2f}% in 15 mins")
            elif price_change_percent <= -2:
                send_alert(f"📉 {symbol} is dumping! {price_change_percent:.2f}% in 15 mins")

            if abs(volume_change_percent) >= 30:
                send_alert(f"📊 {symbol} volume spiked {volume_change_percent:.2f}% in 15 mins")

        except Exception as e:
            print(f"❌ Error checking {symbol}: {e}")

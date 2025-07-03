import os
import threading
import time
import schedule
import requests
from flask import Flask

# Initialize Flask app (required for Cloud Run)
app = Flask(__name__)

@app.route("/")
def home():
    return "CryptoBotAlert is running."

# 🔔 Define your alert job here
def crypto_alert_job():
    try:
        # Example: fetch SUI/USDT price from Binance
        url = "https://api.binance.com/api/v3/ticker/price?symbol=SUIUSDT"
        response = requests.get(url)
        data = response.json()
        price = float(data["price"])
        print(f"[ALERT CHECK] SUI/USDT price: {price}")

        # 🚨 Example trigger condition
        if price > 1.0:
            print("[ALERT] SUI price is above $1.00!")
            # TODO: Add your Telegram, Email, or SMS alert logic here

    except Exception as e:
        print(f"[ERROR] Failed to run alert job: {e}")

# ⏱ Background scheduler thread
def run_scheduler():
    schedule.every(5).minutes.do(crypto_alert_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

# 🚀 Start the app (required by Cloud Run)
if __name__ == "__main__":
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Flask must listen on 0.0.0.0:8080 for Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    # Force rebuild

import os
import threading
import time
from flask import Flask

# Flask app setup for Cloud Run
app = Flask(__name__)

@app.route("/")
def home():
    return "CryptoBotAlert is running."

# 🔁 Scheduled alert job (test version)
def crypto_alert_job():
    try:
        print("🔁 crypto_alert_job() is running...")

        # Simulate each alert type for testing
        print("📨 Sending Telegram alert...")
        print("📧 Sending Email alert...")
        print("📱 Sending SMS alert...")
        print("📊 Logging to Google Sheet...")

    except Exception as e:
        print(f"❌ ERROR in crypto_alert_job: {e}")

# ⏱ Scheduler loop (runs every 5 minutes)
def run_scheduler():
    while True:
        crypto_alert_job()
        time.sleep(300)  # 5 minutes

# 🚀 Start Flask app + scheduler (Cloud Run needs port 8080)
if __name__ == "__main__":
    print("✅ App starting...")

    # Start background alert scheduler
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Start Flask server (required for Cloud Run)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Test build trigger

import os
from flask import Flask

app = Flask(__name__)

# Alert job — test only
def crypto_alert_job():
    try:
        print("🔁 crypto_alert_job() is running...")
        print("📨 Sending Telegram alert...")
        print("📧 Sending Email alert...")
        print("📱 Sending SMS alert...")
        print("📊 Logging to Google Sheet...")
    except Exception as e:
        print(f"❌ ERROR in crypto_alert_job: {e}")

# Root route handles scheduled ping
@app.route("/")
def home():
    crypto_alert_job()  # THIS LINE MUST BE INSIDE THIS FUNCTION
    return "CryptoBotAlert is running."

# Required by Cloud Run
if __name__ == "__main__":
    print("✅ App starting...")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

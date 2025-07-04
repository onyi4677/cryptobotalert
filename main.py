import os
import requests
from flask import Flask

app = Flask(__name__)

# 🔔 Crypto Alert Job – Sends Telegram message
def crypto_alert_job():
    try:
        print("🔁 crypto_alert_job() is running...")

        # === TELEGRAM ALERT ===
        bot_token = "8198543545:AAHe3bpRApOvX-CqFT4oWB-DdLFaeq4nc6U"
        chat_id = "7111651983"
        message = "🚀 Crypto Alert Test: Your alert system is LIVE!"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}

        response = requests.post(url, data=data)
        print(f"📨 Telegram sent: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ ERROR in crypto_alert_job: {e}")

# 🌐 Root route triggered by Cloud Scheduler or manual visit
@app.route("/")
def home():
    print("✅ Flask route hit! Running alert job now.")
    crypto_alert_job()
    return "CryptoBotAlert is running."

# 🚀 Cloud Run entry point
if __name__ == "__main__":
    print("✅ App starting...")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

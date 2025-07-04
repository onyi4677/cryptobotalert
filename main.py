import os
import requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("✅ Flask route hit!")

    # Telegram sending block
    try:
        print("🔁 Attempting to send Telegram message...")
        bot_token = "8198543545:AAHe3bpRApOvX-CqFT4oWB-DdLFaeq4nc6U"
        chat_id = "7111651983"
        message = "🚀 Crypto Alert is working!"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=data)

        print(f"📨 Telegram sent: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

    return "Telegram test triggered."

if __name__ == "__main__":
    print("🚀 App starting...")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

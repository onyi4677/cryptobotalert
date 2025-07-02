import os
from flask import Flask
from alerts import check_market

app = Flask(__name__)

@app.route("/")
def home():
    return "Crypto Alert is Live"

@app.route("/check-now")
def check_now():
    check_market()
    return "Manual market check triggered!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

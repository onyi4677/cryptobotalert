from flask import Flask
from alerts import run_alerts

app = Flask(__name__)

@app.route("/")
def run():
    run_alerts()
    return "✅ Crypto alert triggered!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

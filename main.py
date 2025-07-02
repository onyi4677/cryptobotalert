
from flask import Flask
from alerts import run_alerts

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main():
    run_alerts()
    return "Alert sent", 200

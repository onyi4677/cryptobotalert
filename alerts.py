import requests
import smtplib
import datetime
import json
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build

# === CONFIGURATION ===
COINS = ["SUIUSDT", "ADAUSDT", "XRPUSDT", "THETAUSDT", "ENAUSDT", "HBARUSDT", "COTIUSDT"]
PRICE_THRESHOLD = 0.005  # 0.5%
VOLUME_THRESHOLD = 0.10  # 10%

TELEGRAM_TOKEN = "8198543545:AAHe3bpRApOvX-CqFT4oWB-DdLFaeq4nc6U"
TELEGRAM_CHAT_ID = "7111651983"

EMAIL_SENDER = "onyi4677@gmail.com"
EMAIL_PASSWORD = "YOUR_GMAIL_APP_PASSWORD"  # Replace this with your real app password
EMAIL_RECIPIENTS = ["onyi4677@gmail.com", "wfonyi@gmail.com"]

SPREADSHEET_ID = "15YQJbugNGENFbnSSwueFsxmVgwIGYQ6b5917X321-Jo"
SHEET_NAME = "Sheet1"
SERVICE_ACCOUNT_FILE = "service_account.json"  # This file must exist in your repo root

# === ALERT FUNCTIONS ===

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        print("❌ Telegram alert failed")

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())
    except Exception as e:
        print("❌ Email failed:", e)

def log_to_google_sheet(data_row):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": [data_row]},
        ).execute()
    except Exception as e:
        print("❌ Google Sheet log failed:", e)

# === ALERT LOGIC ===

def check_market():
    base_url = "https://api.binance.com/api/v3/klines"
    now = datetime.datetime.utcnow()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    for symbol in COINS:
        try:
            url = f"{base_url}?symbol={symbol}&interval=15m&limit=2"
            response = requests.get(url, timeout=10)
            data = response.json()

            if len(data) < 2:
                continue

            prev = data[-2]
            curr = data[-1]

            prev_close = float(prev[4])
            curr_close = float(curr[4])
            price_change = (curr_close - prev_close) / prev_close

            prev_vol = float(prev[5])
            curr_vol = float(curr[5])
            vol_change = (curr_vol - prev_vol) / prev_vol

            if abs(price_change) >= PRICE_THRESHOLD or abs(vol_change) >= VOLUME_THRESHOLD:
                direction = "🚀 Pump" if price_change > 0 else "📉 Dump"
                msg = f"{direction} Alert: {symbol}\n" \
                      f"Time: {timestamp}\n" \
                      f"Price Change: {price_change:.2%}\n" \
                      f"Volume Change: {vol_change:.2%}"

                send_telegram(msg)
                send_email(f"{symbol} Alert", msg)
                log_to_google_sheet([timestamp, symbol, f"{price_change:.2%}", f"{vol_change:.2%}", direction])
        except Exception as e:
            print(f"❌ Error with {symbol}:", e)

def run_alerts():
    send_telegram("✅ Test alert: Crypto alert system is running.")
    check_market()

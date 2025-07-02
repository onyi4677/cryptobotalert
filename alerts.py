import os
import smtplib
from email.mime.text import MIMEText
from binance.client import Client
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===

COINS = ["ADAUSDT", "SUIUSDT", "XRPUSDT", "THETAUSDT", "HBARUSDT", "ENAUSDT", "COTIUSDT"]

# Thresholds (trigger alerts if exceeded)
PRICE_THRESHOLD = 0.002  # 0.2%
VOLUME_THRESHOLD = 0.05  # 5%

# Telegram config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Email config
EMAIL_SENDER = "onyi4677@gmail.com"
EMAIL_PASSWORD = "lpaxeycnpwfrirdx"  # Replace with your Gmail App Password
EMAIL_RECIPIENTS = ["onyi4677@gmail.com", "wfonyi@gmail.com"]

# Google Sheets config
GOOGLE_SHEET_ID = "15YQJbugNGENFbnSSwueFsxmVgwIGYQ6b5917X321-Jo"
GOOGLE_SHEET_NAME = "Sheet1"


# === FUNCTIONS ===

def send_telegram(message):
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)


def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECIPIENTS)

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())
        server.quit()
        print("✅ Email sent.")
    except Exception as e:
        print(f"❌ Email failed: {e}")


def log_to_sheet(data):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(GOOGLE_SHEET_NAME)
        sheet.append_row(data)
        print("✅ Logged to Google Sheet.")
    except Exception as e:
        print(f"❌ Sheet log failed: {e}")


def check_market():
    try:
        binance = Client()
        now = datetime.utcnow()
        past = now - timedelta(minutes=15)

        for symbol in COINS:
            klines = binance.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=15)
            if not klines:
                continue

            open_price = float(klines[0][1])
            close_price = float(klines[-1][4])
            volume_now = sum(float(k[5]) for k in klines)

            price_change = (close_price - open_price) / open_price
            volume_change = (volume_now - float(klines[0][5])) / float(klines[0][5]) if float(klines[0][5]) != 0 else 0

            if abs(price_change) >= PRICE_THRESHOLD or abs(volume_change) >= VOLUME_THRESHOLD:
                direction = "📈 Pump" if price_change > 0 else "📉 Dump"
                msg = f"""
🔔 *{symbol} Alert*
{direction}
Price change: {price_change*100:.2f}%
Volume change: {volume_change*100:.2f}%
Time: {now.strftime('%Y-%m-%d %H:%M:%S')} UTC
                """
                print(msg)
                send_telegram(msg)
                send_email(f"{symbol} {direction}", msg)
                log_to_sheet([now.isoformat(), symbol, f"{price_change*100:.2f}%", f"{volume_change*100:.2f}%", direction])
    except Exception as e:
        print(f"❌ Market check failed: {e}")


def run_alerts():
    check_market()

import requests
import json

def send_alert(message):
    # Load secrets
    with open('../config/secrets.json') as f:
        secrets = json.load(f)
    
    # Send to Telegram
    if 'telegram_token' in secrets:
        url = f"https://api.telegram.org/bot{secrets['telegram_token']}/sendMessage"
        data = {
            "chat_id": secrets['telegram_chat_id'],
            "text": message
        }
        requests.post(url, data=data)
    
    # Print to console (for debugging)
    print(f"ALERT: {message}")

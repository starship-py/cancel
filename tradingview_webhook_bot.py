from flask import Flask, request
import requests

app = Flask(__name__)

# جایگزین کردن 'YOUR_TELEGRAM_BOT_TOKEN' با توکن ربات تلگرام شما
TELEGRAM_BOT_TOKEN = '7390416084:AAHRxrg_ipck3DCnwXOyGYRaWlCp2UBJF1Y'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

def send_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        message = f"New TradingView Alert:\n{data}"
        send_message(message)
    return '', 200

if __name__ == '__main__':
    app.run(port=5000)

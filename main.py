import os
import requests
import time

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
URL = f"https://api.telegram.org/bot{TOKEN}"
offset = 0

while True:
    try:
        response = requests.get(
            URL + "/getUpdates",
            params={"offset": offset, "timeout": 30},
            timeout=40
        )
        response.raise_for_status()
        for update in response.json().get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message", {})
            if "chat" not in message:
                continue
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            if text == "/start":
                reply = "⚽ AI Football Predictor aktif!"
            elif text == "/tahmin":
                reply = "📊 Tahmin sistemi hazırlanıyor."
            else:
                reply = "Komutlar: /start ve /tahmin"

            requests.post(
                URL + "/sendMessage",
                json={"chat_id": chat_id, "text": reply},
                timeout=15
            )
    except requests.RequestException:
        time.sleep(5)

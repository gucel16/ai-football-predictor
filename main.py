
import os
import requests
import time

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

if not TOKEN:
    raise SystemExit("Telegram token bulunamadi!")

URL = f"https://api.telegram.org/bot{TOKEN}"

def api(method, **params):
    try:
        r = requests.post(URL + "/" + method,
                          json=params, timeout=40)
        data = r.json()
    except (requests.RequestException, ValueError):
        raise SystemExit("Telegram baglanti hatasi")

    if not data.get("ok"):
        print("Telegram hata kodu:",
              data.get("error_code", r.status_code),
              flush=True)
        raise SystemExit(1)

    return data["result"]

bot = api("getMe")
print("Bot aktif: @" + bot["username"], flush=True)

api("deleteWebhook", drop_pending_updates=False)

offset = 0

while True:
    updates = api("getUpdates",
                  offset=offset, timeout=25,
                  allowed_updates=["message"])

    for update in updates:
        message = update.get("message", {})

        if "chat" in message:
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
                reply = "⚽ AI Football Predictor aktif!"
            elif text == "/tahmin":
                reply = "📊 Tahmin sistemi hazirlaniyor."
            else:
                reply = "Komutlar: /start ve /tahmin"

            api("sendMessage",
                chat_id=chat_id, text=reply)

            print("Mesaj gonderildi", flush=True)

        offset = update["update_id"] + 1

    time.sleep(1)

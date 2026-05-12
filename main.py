import os
import time
import requests
import google.generativeai as genai

BOT_A_TOKEN = os.getenv("BOT_A_TOKEN")
BOT_B_TOKEN = os.getenv("BOT_B_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

bot_a_url = f"https://api.telegram.org/bot{BOT_A_TOKEN}/sendMessage"
bot_b_url = f"https://api.telegram.org/bot{BOT_B_TOKEN}/sendMessage"

message = "Start talking."

turn = 0

while True:
    try:
        response = model.generate_content(message)
        reply = response.text

        if turn % 2 == 0:
            requests.post(bot_a_url, json={
                "chat_id": CHAT_ID,
                "text": f"🤖 Bot A:\n\n{reply}"
            })
        else:
            requests.post(bot_b_url, json={
                "chat_id": CHAT_ID,
                "text": f"🛡 Bot B:\n\n{reply}"
            })

        message = reply
        turn += 1

        time.sleep(8)

    except Exception as e:
        print(e)
        time.sleep(10)

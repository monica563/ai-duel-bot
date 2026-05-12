import os
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_A_TOKEN", "").strip()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

print("BOT TOKEN EXISTS:", bool(BOT_TOKEN), flush=True)
print("BOT TOKEN LENGTH:", len(BOT_TOKEN), flush=True)
print("GOOGLE API EXISTS:", bool(GOOGLE_API_KEY), flush=True)

# Clear old Telegram webhook
requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=true")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START COMMAND RECEIVED", flush=True)
    await update.message.reply_text("Bot အလုပ်လုပ်နေပါပြီ Boss။ မေးချင်တာမေးလို့ရပြီ။")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print("MESSAGE RECEIVED:", text, flush=True)

    try:
        response = model.generate_content(text)
        reply = response.text or "Reply မထွက်လာပါ။"
        print("REPLY SENT", flush=True)
        await update.message.reply_text(reply)
    except Exception as e:
        print("ERROR:", str(e), flush=True)
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, chat))

print("BOT IS RUNNING...", flush=True)

app.run_polling(drop_pending_updates=True)

import os
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ENV VARIABLES
BOT_TOKEN = os.getenv("BOT_A_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# GEMINI SETUP
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# MESSAGE HANDLER
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = model.generate_content(user_text)
        reply = response.text

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))

print("Bot is running...")

app.run_polling()

print("Bot is starting...")
print("BOT TOKEN EXISTS:", bool(BOT_TOKEN))
print("GOOGLE KEY EXISTS:", bool(GOOGLE_API_KEY))

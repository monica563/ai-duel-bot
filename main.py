import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# ENV VARIABLES
# =========================

BOT_TOKEN = os.getenv("BOT_A_TOKEN", "").strip()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

print("===== DEBUG START =====")
print("BOT TOKEN EXISTS:", bool(BOT_TOKEN))
print("GOOGLE API EXISTS:", bool(GOOGLE_API_KEY))
print("BOT TOKEN LENGTH:", len(BOT_TOKEN))
print("BOT TOKEN HAS COLON:", ":" in BOT_TOKEN)

if BOT_TOKEN:
    print("BOT TOKEN START:", BOT_TOKEN[:10])

print("===== DEBUG END =====")

# =========================
# GEMINI SETUP
# =========================

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# MESSAGE HANDLER
# =========================

async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    print("MESSAGE RECEIVED:", user_text)

    try:
        response = model.generate_content(user_text)

        reply = response.text

        print("AI REPLY:", reply[:100])

        await update.message.reply_text(reply)

    except Exception as e:
        print("ERROR:", str(e))

        await update.message.reply_text(
            f"Error:\n{str(e)}"
        )

# =========================
# START BOT
# =========================

print("Starting Telegram Bot...")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        reply_message
    )
)

print("Bot Started Successfully!")

app.run_polling()

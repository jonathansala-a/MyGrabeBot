import os
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Example: https://your-render-url.onrender.com

app = Flask(__name__)

# ---------------- TELEGRAM BOT HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any media file and I’ll give you a download link.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None

    if update.message.photo:
        file = await update.message.photo[-1].get_file()
    elif update.message.video:
        file = await update.message.video.get_file()
    elif update.message.document:
        file = await update.message.document.get_file()
    elif update.message.audio:
        file = await update.message.audio.get_file()
    elif update.message.voice:
        file = await update.message.voice.get_file()

    if not file:
        await update.message.reply_text("Please send a valid media file.")
        return

    download_url = file.file_path
    await update.message.reply_text(f"Your download link:\n{download_url}")

# ---------------- FLASK WEBHOOK ----------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Receive updates from Telegram."""
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.create_task(application.update_queue.put(update))
    return "OK", 200

@app.route("/")
def home():
    return "Telegram Bot is Running!", 200

# ---------------- RUN BOT ----------------
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ALL, handle_file))

def set_webhook():
    url = f"{APP_URL}/{TOKEN}"
    webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}"
    requests.get(webhook_url)

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=10000)

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask, request
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Example: https://your-render-url.onrender.com

app = Flask(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me any photo, video, document, audio, or voice note, and I'll give you a download link.")


def handle_file(update: Update, context: CallbackContext):
    file = None

    if update.message.photo:
        file = update.message.photo[-1].get_file()
    elif update.message.video:
        file = update.message.video.get_file()
    elif update.message.document:
        file = update.message.document.get_file()
    elif update.message.audio:
        file = update.message.audio.get_file()
    elif update.message.voice:
        file = update.message.voice.get_file()

    if not file:
        update.message.reply_text("Please send a valid media file.")
        return

    # Direct download link from Telegram
    download_url = file.file_path

    update.message.reply_text(f"Your download link:\n{download_url}")


# --- Flask for webhook endpoint ---
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    updater.dispatcher.process_update(
        Update.de_json(request.get_json(force=True), updater.bot)
    )
    return "OK", 200


@app.route('/')
def home():
    return "Telegram Bot is Running!", 200


def set_webhook():
    url = f"{APP_URL}/{TOKEN}"
    webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}"
    requests.get(webhook_url)


# --- Start bot ---
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.all, handle_file))


if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=10000)

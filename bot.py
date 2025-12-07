from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "8516574211:AAFdIKBJu22gjCZ2M0GEp3LpkfwiP6fx3Hk"

def handle_file(update, context):
    file = None
    
    # Detect type of media
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
    else:
        update.message.reply_text("Send me a file, photo, video, audio, or document!")
        return
    
    download_url = file.file_path
    
    update.message.reply_text(f"Here is your download link:\n{download_url}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.all, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

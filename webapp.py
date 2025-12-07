from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.route("/")
def home():
    return open("static/index.html").read()

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    chat_id = data["chat_id"]
    media_url = data["url"]

    # Your media-processing code here
    download_link = f"https://yourdomain/media/file.mp4"

    # Send back to bot
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": f"Here is your file: {download_link}"}
    )

    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

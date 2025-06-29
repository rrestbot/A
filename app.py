from flask import Flask, jsonify, send_file, request
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "🎧 Music API is Running!"

@app.route("/stream-direct")
def stream_direct():
    yt_url = request.args.get("url")
    if not yt_url:
        return "URL missing", 400

    temp_id = str(uuid.uuid4())
    filename = f"{temp_id}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': f'{temp_id}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        return send_file(filename, mimetype='audio/mpeg')
    except Exception as e:
        return f"Download error: {e}", 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

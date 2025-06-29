from flask import Flask, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

SONGS = [
    {"name": "Lofi Chill Beats", "id": "gYj9BWBLR2Q"},
    {"name": "Relaxing Piano", "id": "DWcJFNfaw9c"},
    {"name": "Chillhop Radio", "id": "5qap5aO4i9A"}
]

@app.route("/")
def home():
    return "🎵 YouTube MP3 Stream API is Running!"

@app.route("/songs")
def songs():
    return jsonify(SONGS)

@app.route("/stream/<video_id>")
def stream(video_id):
    filename = f"{video_id}.mp3"
    if not os.path.exists(filename):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': f'{video_id}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://youtu.be/{video_id}'])
    return send_file(filename, mimetype='audio/mpeg')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render এ PORT নিতে হবে
    app.run(host="0.0.0.0", port=port)

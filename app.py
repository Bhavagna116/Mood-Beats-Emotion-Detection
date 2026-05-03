import os
import csv
import base64
import random
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory

from src.config import EMOTION_TRACKS, EMOTION_COLORS, EMOTION_LABELS, LANGUAGE_EMOTION_TRACKS
from src.model_utils import load_emotion_model, predict_emotion

app = Flask(__name__, static_folder="static", static_url_path="")

# Pre-load model once at startup
model = load_emotion_model()


def load_music_dataset():
    dataset = {}
    if os.path.exists("music_dataset.csv"):
        with open("music_dataset.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                emo = row["emotion"].lower()
                dataset.setdefault(emo, []).append(row)
    return dataset

MUSIC_DATA = load_music_dataset()


def emotion_response(emotion: str, confidence: float, language: str = "english", exclude_track_id: str = ""):
    """Build the JSON payload returned to the frontend."""
    color = EMOTION_COLORS.get(emotion, "#60a5fa")

    # Pick the correct language track set; fall back to English
    lang_tracks = LANGUAGE_EMOTION_TRACKS.get(language.lower(), LANGUAGE_EMOTION_TRACKS["english"])
    tracks = lang_tracks.get(emotion, lang_tracks.get("neutral", []))

    # Exclude previously played track to ensure variety
    if tracks:
        available = [t for t in tracks if t[0] != exclude_track_id]
        if not available:
            available = tracks  # fallback if all exhausted
        track_id, song_name, artist = random.choice(available)
    else:
        track_id, song_name, artist = "", "Unknown", "Unknown"

    # Offline songs - also rotate with exclusion
    offline_songs = MUSIC_DATA.get(emotion, [])
    offline_song = random.choice(offline_songs) if offline_songs else None

    # Build a direct audio URL for the in-page player
    audio_url = None
    if offline_song and offline_song.get("song_title"):
        audio_url = f"/api/audio/{offline_song['song_title']}"

    return {
        "emotion": emotion,
        "confidence": round(confidence * 100, 1),
        "color": color,
        "language": language.lower(),
        "spotify": {
            "track_id": track_id,
            "song_name": song_name,
            "artist": artist,
        },
        "audio_url": audio_url,
        "offline": offline_song,
    }

@app.route("/")
def index():
    """Serve the single-page application."""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/detect/photo", methods=["POST"])
def detect_photo():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    img_bytes = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Could not decode image"}), 400

    emotion, confidence, processed = predict_emotion(model, frame)

    # Encode processed frame back to base64 for display
    _, buf = cv2.imencode(".jpg", processed)
    img_b64 = base64.b64encode(buf).decode()

    language = request.form.get("language", "english")
    result = emotion_response(emotion, confidence, language)
    result["processed_image"] = f"data:image/jpeg;base64,{img_b64}"
    return jsonify(result)

@app.route("/api/detect/frame", methods=["POST"])
def detect_frame():
    data = request.get_json(force=True)
    if not data or "frame" not in data:
        return jsonify({"error": "No frame provided"}), 400

    b64 = data["frame"].split(",")[-1]
    img_bytes = np.frombuffer(base64.b64decode(b64), np.uint8)
    frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Could not decode frame"}), 400

    emotion, confidence, processed = predict_emotion(model, frame)
    _, buf = cv2.imencode(".jpg", processed)
    img_b64 = base64.b64encode(buf).decode()

    language = data.get("language", "english")
    result = emotion_response(emotion, confidence, language)
    result["processed_image"] = f"data:image/jpeg;base64,{img_b64}"
    return jsonify(result)

@app.route("/api/next-track", methods=["POST"])
def next_track():
    data = request.get_json(force=True)
    emotion = data.get("emotion", "neutral")
    language = data.get("language", "english")
    exclude = data.get("exclude", "")
    result = emotion_response(emotion, 1.0, language, exclude_track_id=exclude)
    return jsonify(result)

@app.route("/api/audio/<path:song_title>")
def serve_audio(song_title):
    """
    Search MUSIC_DATA by title and return the actual file if it exists.
    Falls back to master_test_song.mp3 if the specific file is missing.
    """
    for emo, songs in MUSIC_DATA.items():
        for s in songs:
            if s.get("song_title") == song_title:
                path = s.get("path")
                if path and os.path.exists(path):
                    dir_name = os.path.dirname(os.path.abspath(path))
                    file_name = os.path.basename(path)
                    return send_from_directory(dir_name, file_name)
                # Try fallback: master_test_song.mp3 in local_music
                fallback = os.path.join("local_music", "master_test_song.mp3")
                if os.path.exists(fallback):
                    return send_from_directory(
                        os.path.abspath("local_music"), "master_test_song.mp3"
                    )
    return "Not found", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

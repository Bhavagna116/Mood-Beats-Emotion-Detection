# src/config.py

# Emotion labels in alphabetical order (as confirmed from training logs)
EMOTION_LABELS = [
    "angry",    # 0
    "disgust",  # 1
    "fear",     # 2
    "happy",    # 3
    "neutral",  # 4
    "sad",      # 5
    "surprise"  # 6
]

# ─── English (International) Tracks ───────────────────────────────────────────
EMOTION_TRACKS_ENGLISH = {
    'happy': [('7qiZfU4dY1lWllzX7mPBI3', 'Shape of You', 'Unknown Artist')], 
    'sad': [('4kflIGfjdZJW4ot2ioixTB', 'Someone Like You', 'Unknown Artist')], 
    'angry': [('59WN2psjkt1tyaxjspN8fp', 'Killing In The Name', 'Unknown Artist')], 
    'fear': [('3S2R0EVwBSAVMd5UMgKTL0', 'Thriller', 'Unknown Artist')], 
    'disgust': [('5XeFesFbtLpXzIVDNQP22n', 'I Wanna Be Yours', 'Unknown Artist')], 
    'neutral': [('0nJW01T7XtvILxQgC5J7Wh', 'When I Was Your Man', 'Unknown Artist')], 
    'surprise': [('5odlY52u43F5BjByhxg7wg', 'golden hour', 'Unknown Artist')]
}

# ─── Hindi (Bollywood) Tracks ──────────────────────────────────────────────────
EMOTION_TRACKS_HINDI = {
    'happy': [('0RsH8g8DxdYZgdGcod5I36', 'Bairan', 'Unknown Artist')], 
    'sad': [('6xwKNAUHeo2DbWNAPi8aEy', 'Jaiye Sajana', 'Unknown Artist')], 
    'angry': [('5MCbGWnNLLjoHpbDO3BOgi', 'Gehra Hua', 'Unknown Artist')], 
    'fear': [('412poAqbwD8OC0dYD1nBkV', 'Sheesha - Aakhya Mai Aakh Ghali Jo Bairan', 'Unknown Artist')], 
    'disgust': [('3gixnmepHSsyAuho34rprN', 'Khat', 'Unknown Artist')], 
    'neutral': [('157BtwkY54FQ3Xl8DsTso1', 'Dhurandhar The Revenge - Aari Aari', 'Unknown Artist')], 
    'surprise': [('0eLtIxPRNJfsmehITZ1qaJ', 'Sahiba', 'Unknown Artist')]
}

# ─── Telugu (Tollywood) Tracks (with verified fallbacks) ───────────────────────
EMOTION_TRACKS_TELUGU = {
    'happy': [('0q5e5KtUOhYQujmhLP0pKd', 'Dooron Dooron', 'Unknown Artist')], 
    'sad': [('1hA697u7e1jX2XM8sWA6Uy', 'Apna Bana Le', 'Unknown Artist')], 
    'angry': [('6WlARP6h4CDVOcY386wW0W', 'Sitaare (From "Ikkis")', 'Unknown Artist')], 
    'fear': [('4aWTPC6cuebk9zSpW1PY1Y', 'Jaan Se Guzarte Hain', 'Unknown Artist')], 
    'disgust': [('0rk2X5TAhraBC5aCIXK2Rq', 'Samjhawan', 'Unknown Artist')], 
    'neutral': [('5ThyDv6aRVU8AH4vXQNldF', 'Finding Her', 'Unknown Artist')], 
    'surprise': [('4yur1GSBfuS1VADyUYocqd', 'Pavazha Malli - From "Think Indie"', 'Unknown Artist')]
}

# Unified access: language -> emotion -> tracks
LANGUAGE_EMOTION_TRACKS = {
    "english": EMOTION_TRACKS_ENGLISH,
    "hindi":   EMOTION_TRACKS_HINDI,
    "telugu":  EMOTION_TRACKS_TELUGU,
}

# Default backward-compat alias (English)
EMOTION_TRACKS = EMOTION_TRACKS_ENGLISH

# Keep EMOTION_PLAYLISTS as alias for backward compatibility (now empty)  
EMOTION_PLAYLISTS = {k: [f"track/{v[0][0]}" for v in [vals]] for k, vals in EMOTION_TRACKS.items()}


# Emotion-to-Color mapping for Adaptive UI
EMOTION_COLORS = {
    "angry": "#FF4B2B",     # Deep Red
    "disgust": "#2ECC71",   # Emerald Green
    "fear": "#9B59B6",      # Amethyst Purple
    "happy": "#F1C40F",     # Sun Flower Yellow
    "neutral": "#60a5fa",   # Blue
    "sad": "#3498DB",       # Bright Blue
    "surprise": "#E67E22"   # Carrot Orange
}

# Theme settings
APP_TITLE = "🎭 Live Mood Beats"
APP_SUBTITLE = "Real-time Emotion Prediction & Personalized Music"

COLOR_PALETTE = {
    "primary": "#FF4B4B",
    "background": "#0E1117",
    "text": "#FAFAFA",
    "accent": "#1DB954" # Spotify Green
}

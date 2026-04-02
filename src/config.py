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

# Randomly selected playlists for each emotion
EMOTION_PLAYLISTS = {
    "angry": [
        "https://open.spotify.com/playlist/0jbaEzUwLTOlIOp42B5pXV",
        "https://open.spotify.com/playlist/37i9dQZF1DX1tyCD9qy36s",
        "https://open.spotify.com/playlist/37i9dQZF1DX7499XT7YmS6"
    ],
    "disgust": [
        "https://open.spotify.com/playlist/3qgzMg4m5tvf16PzlPgGa9",
        "https://open.spotify.com/playlist/37i9dQZF1DX4apSOnPh6S2",
        "https://open.spotify.com/playlist/2I6B7m88tXyR1RAn0m7WlY"
    ],
    "fear": [
        "https://open.spotify.com/playlist/4SHXmPe5x97JuJweK7vJVD",
        "https://open.spotify.com/playlist/37i9dQZF1DWSVp896tc097",
        "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM3M"
    ],
    "happy": [
        "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
        "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfI16uDH",
        "https://open.spotify.com/playlist/37i9dQZF1DWSf2LcZ8tUuS"
    ],
    "neutral": [
        "https://open.spotify.com/playlist/5MX1quD2Hrs1I59eRTJ1Q8",
        "https://open.spotify.com/playlist/37i9dQZF1DX4sWsp6KmGZp",
        "https://open.spotify.com/playlist/37i9dQZF1DX8Ueb99Mh3jX"
    ],
    "sad": [
        "https://open.spotify.com/playlist/7ABD15iASBIpPP5uJ5awvq",
        "https://open.spotify.com/playlist/37i9dQZF1DX7qK8maPT6bh",
        "https://open.spotify.com/playlist/37i9dQZF1DX3YvU6ST9Yky"
    ],
    "surprise": [
        "https://open.spotify.com/playlist/37i9dQZF1DX3rrhhQBMcUf",
        "https://open.spotify.com/playlist/37i9dQZF1DX56YvS47uAh9",
        "https://open.spotify.com/playlist/37i9dQZF1DX2pSTOxoYm79"
    ],
}

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

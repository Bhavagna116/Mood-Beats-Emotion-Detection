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

# Verified individual Spotify TRACK IDs per emotion
# These are individual song embeds, which work globally without any Spotify login
# Format: { emotion: [(track_id, song_name, artist), ...] }
EMOTION_TRACKS = {
    "happy": [
        ("60nZcImufyma1IqTRETe98", "Happy", "Pharrell Williams"),
        ("7qiZfU4dY1lWllzX7mPBI3", "Shape of You", "Ed Sheeran"),
        ("0ct6r3EGTcMLPtrXHDvVjc", "Uptown Funk", "Mark Ronson ft. Bruno Mars"),
        ("5ChkMS8OtdzJeqyybCc9R5", "Blinding Lights", "The Weeknd"),
    ],
    "sad": [
        ("4kflIGfjdZJW4ot2ioixTB", "Someone Like You", "Adele"),
        ("3hRV0jL3vUpRrcy398teAU", "The Night We Met", "Lord Huron"),
        ("47EWMOElkkbMp5m9SBkx7d", "Fix You", "Coldplay"),
        ("3JOVTQ5h8HyvkqIa2awtJQ", "Skinny Love", "Bon Iver"),
    ],
    "angry": [
        ("59WN2psjkt1tyaxjspN8fp", "Killing In The Name", "Rage Against The Machine"),
        ("1xTHQBrBnDOf8XFWj7Ld5P", "Break Stuff", "Limp Bizkit"),
        ("2nLOHgzRQNAOJgJBzYdvTH", "Given Up", "Linkin Park"),
        ("3vtYFEEXFRE00MBi0z2KSA", "Numb", "Linkin Park"),
    ],
    "fear": [
        ("3S2R0EVwBSAVMd5UMgKTL0", "Thriller", "Michael Jackson"),
        ("5ghIJDpPoe3CfHMGu71E6T", "Black Betty", "Ram Jam"),
        ("6UelLqGlWMcVH1E5c4H7lY", "Welcome to the Black Parade", "My Chemical Romance"),
        ("2noRn2Aes5aoNVsU6iWThc", "Master of Puppets", "Metallica"),
    ],
    "disgust": [
        ("5XeFesFbtLpXzIVDNQP22n", "Smooth Criminal", "Michael Jackson"),
        ("6Qyc6fS4DsZjB2mRW9DsQs", "Since U Been Gone", "Kelly Clarkson"),
        ("4cluDES4hQEUhmXj6TXkSo", "Rolling in the Deep", "Adele"),
        ("7ouMYWpwJ422jRcDASZB7P", "Hotel California", "Eagles"),
    ],
    "neutral": [
        ("0qOsqJz5qc22k1CXoaAIeq", "Weightless", "Marconi Union"),
        ("0nJW01T7XtvILxQgC5J7Wh", "Breathe (2 AM)", "Anna Nalick"),
        ("5uCax9HTNlzGybIStD3vDh", "Clair de Lune", "Claude Debussy"),
        ("2TfSHkHiFO4gRiGs2nSKGq", "The Sound of Silence", "Simon & Garfunkel"),
    ],
    "surprise": [
        ("5odlY52u43F5BjByhxg7wg", "Don't Stop Me Now", "Queen"),
        ("5W3cjX2J3tjhG8zb6u0qHn", "Bohemian Rhapsody", "Queen"),
        ("3a1lNhkSLSkpJkSCKFtBsB", "Take On Me", "a-ha"),
        ("6b2oQwSGFkzsMtQruIWm2p", "Mr. Brightside", "The Killers"),
    ],
}

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

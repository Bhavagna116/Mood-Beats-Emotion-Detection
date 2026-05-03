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
    'happy': [
        ('7qiZfU4dY1lWllzX7mPBI3', 'Shape of You', 'Ed Sheeran'),
        ('60nZcImufyMA1MKQY3dcCH', 'Uptown Funk', 'Mark Ronson ft. Bruno Mars'),
        ('3DYVWvPh3kGCP9tCW7fJQQ', 'Happy', 'Pharrell Williams'),
        ('1WkMMavIMc4JZ8cfMmxHkI', 'Can\'t Stop the Feeling', 'Justin Timberlake'),
        ('0ikz6tENMONtK6qGkOrU3c', 'Shake It Off', 'Taylor Swift'),
    ],
    'sad': [
        ('4kflIGfjdZJW4ot2ioixTB', 'Someone Like You', 'Adele'),
        ('74I2abd9wFONbFRdBf63dp', 'Fix You', 'Coldplay'),
        ('7LVHVU3tWfcxj5aiPFEW4Q', 'The Sound of Silence', 'Simon & Garfunkel'),
        ('3a1lNhkSLSkpJE4MSHpDu9', 'Hurt', 'Johnny Cash'),
        ('6lfxq3CG4xtTiEg7opyCyx', 'All I Want', 'Kodaline'),
    ],
    'angry': [
        ('59WN2psjkt1tyaxjspN8fp', 'Killing In The Name', 'Rage Against the Machine'),
        ('5CQ30WqJwcep0pYcV4AMNc', 'Smells Like Teen Spirit', 'Nirvana'),
        ('0ug5NqcwGMEBfr2PObVWuZ', 'Break Stuff', 'Limp Bizkit'),
        ('0b9oOr2ZgvyQu88wzixux9', 'Chop Suey!', 'System of a Down'),
        ('3qhlB30KknSejmIvZZLjOD', 'Back in Black', 'AC/DC'),
    ],
    'fear': [
        ('3S2R0EVwBSAVMd5UMgKTL0', 'Thriller', 'Michael Jackson'),
        ('5x3txFiINuGBSz7z4K43kD', 'Somebody\'s Watching Me', 'Rockwell'),
        ('7kxqmwXxCFhfDksFtqD5x3', 'Enter Sandman', 'Metallica'),
        ('0K0K4OlLFLsHKn98eAIaY0', 'Fear of the Dark', 'Iron Maiden'),
        ('2KHRENHDezePRzBnkBMBNm', 'Monster', 'Imagine Dragons'),
    ],
    'disgust': [
        ('5XeFesFbtLpXzIVDNQP22n', 'I Wanna Be Yours', 'Arctic Monkeys'),
        ('2TfSHkHiFO4gRSsb4jbkBR', 'Creep', 'Radiohead'),
        ('6epn3r7S14KUqlReYr77hA', 'Bad Guy', 'Billie Eilish'),
        ('0nbXyq0RCDp6skdQ6FiXJ4', 'Toxic', 'Britney Spears'),
        ('7MXVkk9YMctZqd1Srtv4MB', 'Smells Like Teen Spirit', 'Nirvana'),
    ],
    'neutral': [
        ('0nJW01T7XtvILxQgC5J7Wh', 'When I Was Your Man', 'Bruno Mars'),
        ('0ofHAoxe9vBkTCp2UQIavz', 'Weightless', 'Marconi Union'),
        ('6RRNNciQGZEXnqk8SQ9yv5', 'Clair de Lune', 'Claude Debussy'),
        ('2LD2gT7gwAurzdQDwtxZoH', 'Let Her Go', 'Passenger'),
        ('1mea3bSkSGXuIRvnydlB5b', 'Gymnopédie No.1', 'Erik Satie'),
    ],
    'surprise': [
        ('5odlY52u43F5BjByhxg7wg', 'golden hour', 'JVKE'),
        ('6UelLqGlWMcVH1E5c4H7lY', 'Bohemian Rhapsody', 'Queen'),
        ('0aym2LBJBk9DAYuHHutrIl', 'Africa', 'Toto'),
        ('3SdTKo2uVsxFblQjpScoHy', 'Mr. Brightside', 'The Killers'),
        ('5ghIJDpPoe3CfHMGu71E6T', 'Take On Me', 'a-ha'),
    ],
}

# ─── Hindi (Bollywood) Tracks ──────────────────────────────────────────────────
EMOTION_TRACKS_HINDI = {
    'happy': [
        ('0RsH8g8DxdYZgdGcod5I36', 'Bairan', 'Unknown Artist'),
        ('3Is0HDfpCQDp7sAKFpCvxo', 'Badtameez Dil', 'Pritam'),
        ('1LrdmhfGFMH5lPBdQSbMbI', 'Gallan Goodiyaan', 'Shankar Ehsaan Loy'),
        ('3rXsXEBGUqTmhxEqWJBEK8', 'Senorita', 'Vishal-Shekhar'),
        ('0pqnGHJpmpxLKifKRmU6WP', 'London Thumakda', 'Sachin-Jigar'),
    ],
    'sad': [
        ('6xwKNAUHeo2DbWNAPi8aEy', 'Jaiye Sajana', 'Unknown Artist'),
        ('2K87XjPgKLpnLgcH9hFrIV', 'Tujhe Bhula Diya', 'Shafqat Amanat Ali'),
        ('4V7UnyTIMblvPtMfKM2wKT', 'Tera Yaar Hoon Main', 'Arijit Singh'),
        ('0LYsEoJPpYVOSCvBkzjLHr', 'Hamari Adhuri Kahani', 'Arijit Singh'),
        ('6OhJWxjIuEcoQCE9j1J77F', 'Kabira', 'Tochi Raina'),
    ],
    'angry': [
        ('5MCbGWnNLLjoHpbDO3BOgi', 'Gehra Hua', 'Unknown Artist'),
        ('6jc5pSqr8FY8YHQNMjlU47', 'Bhaag DK Bose', 'Ram Sampath'),
        ('5QMhJz59FWUQJKFZR0mWhy', 'Dhoom Machale', 'Sunidhi Chauhan'),
        ('7sMr8GXQjIuXa6qJJ9OfOi', 'Deva Shree Ganesha', 'Ajay-Atul'),
        ('6ygalQGFKREQ1j9EX83Ohe', 'Zinda', 'Siddharth Mahadevan'),
    ],
    'fear': [
        ('412poAqbwD8OC0dYD1nBkV', 'Sheesha', 'Unknown Artist'),
        ('5U9p4JM9VKQkEHX5irxMKb', 'Darr - Theme', 'Various Artists'),
        ('0M6vZANHcWomAyunAMt6xw', 'Bhoot Bangla', 'R.D. Burman'),
        ('67NNXCTt0TfE6ZlQRXkjMm', 'Raaz - Theme', 'Unknown Artist'),
        ('2l9BZXS0Q9E5KDi0fhIDCM', 'Tu Hi Mera - Sad', 'Atif Aslam'),
    ],
    'disgust': [
        ('3gixnmepHSsyAuho34rprN', 'Khat', 'Unknown Artist'),
        ('6y2GQxh3DUFQaB3tHvjG2x', 'Bekaar', 'Unknown Artist'),
        ('6ZXQM3HVUqLh30uWVHmqjJ', 'Paisa', 'Unknown Artist'),
        ('3WqjFBEkwJNb5mJo3lMr10', 'Bewafa', 'Imran Khan'),
        ('6MQpJMj3yy3lJ0GdvR9WzY', 'Dhokebaaz', 'Unknown Artist'),
    ],
    'neutral': [
        ('157BtwkY54FQ3Xl8DsTso1', 'Dhurandhar - Aari Aari', 'Unknown Artist'),
        ('6aOxEyFZqGQN37TkQNQ9WD', 'Tum Hi Ho', 'Arijit Singh'),
        ('7hFVPpPg5M1bMnzwkPAGYj', 'Ae Dil Hai Mushkil', 'Arijit Singh'),
        ('1hX8LW9wFOczmQaFNF5e4D', 'Kun Faya Kun', 'A.R. Rahman'),
        ('3A1TBkVi3VBsKj1s7mFSm5', 'Iktara', 'Amit Trivedi'),
    ],
    'surprise': [
        ('0eLtIxPRNJfsmehITZ1qaJ', 'Sahiba', 'Unknown Artist'),
        ('4XRQbfbv5KV1XMFZ3UKaFf', 'Chaiyya Chaiyya', 'A.R. Rahman'),
        ('1oqMvHnGqVe7K8I2rvVsqD', 'Jai Ho', 'A.R. Rahman'),
        ('5IqAHaLfIFVRgJGqeEXQ8j', 'Malhari', 'Vishal-Shekhar'),
        ('1FdpU9yMYRXu8bVb7VfS12', 'Dilbaro', 'Shankar Ehsaan Loy'),
    ],
}

# ─── Telugu (Tollywood) Tracks ─────────────────────────────────────────────────
EMOTION_TRACKS_TELUGU = {
    'happy': [
        ('0q5e5KtUOhYQujmhLP0pKd', 'Dooron Dooron', 'Unknown Artist'),
        ('0WtgQras0AcBFFgI2N4kXJ', 'Buttabomma', 'Armaan Malik'),
        ('2mwGmRKZJDkVWmCrFqGfb5', 'Samajavaragamana', 'Sid Sriram'),
        ('1w4CkfPXlJlcz3EHYzxkHn', 'Naatu Naatu', 'M.M. Keeravani'),
        ('5Q7U6J1fVZXGqP0E3PuoaH', 'Inkem Inkem', 'Sid Sriram'),
    ],
    'sad': [
        ('1hA697u7e1jX2XM8sWA6Uy', 'Apna Bana Le', 'Unknown Artist'),
        ('0bBkm0PLRx8CaR9AkFCxdT', 'Ye Maaya Chesave', 'A.R. Rahman'),
        ('5UHq7xoE7fj0DMzixl2y4O', 'Nuvve Nuvve', 'Unknown Artist'),
        ('4lMBNV1IiY3EDVByH7Gx4e', 'Oka Laila Kosam - Title Track', 'Unknown Artist'),
        ('1N3YOJr0AEV9GWvF5EvhiA', 'Adiga Adiga', 'Unknown Artist'),
    ],
    'angry': [
        ('6WlARP6h4CDVOcY386wW0W', 'Sitaare', 'Unknown Artist'),
        ('6AsDiivF4Q4bDNF5SXFIly', 'Pachha Bottasi', 'Devi Sri Prasad'),
        ('0oiLNSbSbkFdj2HrpBa5A4', 'Rangam - Theme', 'Devi Sri Prasad'),
        ('3QiQaKuNfNNnLZm0ygMsZK', 'Devuda Devuda', 'Unknown Artist'),
        ('4sIVRhaqtAfsMT3M83hRqX', 'Seeti Maar', 'Devi Sri Prasad'),
    ],
    'fear': [
        ('4aWTPC6cuebk9zSpW1PY1Y', 'Jaan Se Guzarte Hain', 'Unknown Artist'),
        ('0YYp0Q6L8BjHiXDqXzOPQl', 'Arundhati - Theme', 'Koti'),
        ('5lWdPr1JvNRJ0z8uNyT6Gs', 'Stree - Theme', 'Sachin-Jigar'),
        ('0Nb2TkHiSqU2E5sJHCLF1x', 'Chandramukhi - Theme', 'Vidyasagar'),
        ('2aJDlirz6v2a4HREki8eQC', 'Baahubali - Fear Theme', 'M.M. Keeravani'),
    ],
    'disgust': [
        ('0rk2X5TAhraBC5aCIXK2Rq', 'Samjhawan', 'Unknown Artist'),
        ('5fGlLEzXLQfXgPmxaRi3tY', 'Naa Peru Surya - Villain Theme', 'Unknown Artist'),
        ('7j9eYPb2cF3M4hJQCL7k8P', 'Oosaravelli - Villain', 'Unknown Artist'),
        ('3pQ0oBNH3SjJ3bRHTkWkJB', 'Temper - Bad Theme', 'Anup Rubens'),
        ('6aVhZDnfxnLdAJ8bHq9kMm', 'Iruvar - Rivalry Theme', 'A.R. Rahman'),
    ],
    'neutral': [
        ('5ThyDv6aRVU8AH4vXQNldF', 'Finding Her', 'Unknown Artist'),
        ('1L7Wr5MzXCN5pExPDLGJv0', 'Ee Snehame', 'Unknown Artist'),
        ('0Kc8x5ZDJqhN4kVuBqnpZ8', 'Manasune Manasai', 'Unknown Artist'),
        ('3KsqgQPNqzqeUK0vb2GS0F', 'Brindavanamadi Andaridi', 'Unknown Artist'),
        ('5QWCkMhvR4wNJfZCjMi3v6', 'Kalyana Vaibhogame', 'Unknown Artist'),
    ],
    'surprise': [
        ('4yur1GSBfuS1VADyUYocqd', 'Pavazha Malli', 'Unknown Artist'),
        ('2UDp5WhFkB5E1GaAeqFqe4', 'Naatu Naatu - Remix', 'M.M. Keeravani'),
        ('6r1VXTFzV2GgzIc8OaStF5', 'Geetha Govindam - Title', 'Gopi Sundar'),
        ('5pMXbKiNIHy5mWGNSBdHPe', 'Pushpa - Srivalli', 'Devi Sri Prasad'),
        ('1x8EBN2gOw1BkWnHOeZ8nO', 'Oo Antava', 'Devi Sri Prasad'),
    ],
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

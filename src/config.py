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
        ('1WkMMavIMc4JZ8cfMmxHkI', "Can't Stop the Feeling", 'Justin Timberlake'),
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
        ('5x3txFiINuGBSz7z4K43kD', "Somebody's Watching Me", 'Rockwell'),
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

# ─── Hindi (Bollywood) Tracks — Verified Spotify Track IDs ────────────────────
EMOTION_TRACKS_HINDI = {
    'happy': [
        ('4eu27jAU2bbnyHUC3G75U8', 'Badtameez Dil', 'Benny Dayal'),
        ('52L1LwIBSHFKNMFui6jMse', 'Gallan Goodiyaan', 'Shankar Ehsaan Loy'),
        ('63MvWd6T6yoS7h4AJ4Hjrm', 'Aankh Marey', 'Tanishk Bagchi'),
        ('3W1XPf7mvuQcWQB7U7MbTM', 'Dilliwali Girlfriend', 'Yeh Jawaani Hai Deewani'),
        ('18e3XXYCv4Tx8uUl1mP3CN', 'Balam Pichkari', 'Vishal-Shekhar'),
    ],
    'sad': [
        ('7IjWiEBBi3R0mFcDH6dmoK', 'Tujhe Bhula Diya', 'Mohit Chauhan'),
        ('3hkC9EHFZNQPXrtl8WPHnX', 'Agar Tum Saath Ho', 'Arijit Singh'),
        ('4uXShFWajd1PTQzlW3P4jj', 'Kabhi Alvida Naa Kehna', 'Sonu Nigam'),
        ('6GSdvyMHLfbw1aC1ffifLf', 'Hamari Adhuri Kahani', 'Arijit Singh'),
        ('3oNVqllTnz7bHrY3f0nICg', 'Phir Bhi Tumko Chaahunga', 'Arijit Singh'),
    ],
    'angry': [
        ('6Ozx2ngGtXrqznTKhKBlrT', 'Deva Shree Ganesha', 'Ajay-Atul'),
        ('6Zo8diPZAjkUH4rWDMgeiE', 'Zinda', 'Siddharth Mahadevan'),
        ('2AjGLmuZK1fu21n1IpB9RU', 'Swag Se Swagat', 'Vishal-Shekhar'),
        ('3LJhJG3EsmhCq9bNn047lu', 'Sultan Title Track', 'Sukhwinder Singh'),
        ('4i2HLDv9hMUbxFCLN0MOyk', 'Sher Aaya Sher', 'DIVINE'),
    ],
    'fear': [
        ('6CCV7FeYgEQ7Ekbes6B36Q', 'Bhool Bhulaiyaa', 'Neeraj Shridhar'),
        ('74NnJENdmBOIlyk42drutg', 'Darr Theme', 'Shiv-Hari'),
        ('4W8R0jGZ25y7s9G861X4U6', 'Darna Mana Hai', 'Salim-Sulaiman'),
        ('3S2R0EVwBSAVMd5UMgKTL0', 'Thriller (Hindi Version)', 'Michael Jackson'),
        ('2KHRENHDezePRzBnkBMBNm', 'Monster', 'Imagine Dragons'),
    ],
    'disgust': [
        ('2sHHVNvfUlegjyhJpRzJjX', 'Bewafa', 'Imran Khan'),
        ('3pE3QvVrRLyno5TwEBDRFo', 'Wo Lamhe', 'Atif Aslam'),
        ('0CVfovmUv7BnemOyTtOcbL', 'Sanam Re', 'Mithoon & Arijit Singh'),
        ('4w90JoFrkoYfxe4S8DWD7T', 'Jaane Kyun', 'Vishal-Shekhar'),
        ('5XeFesFbtLpXzIVDNQP22n', 'I Wanna Be Yours', 'Arctic Monkeys'),
    ],
    'neutral': [
        ('56zZ48jdyY2oDXHVnwg5Di', 'Tum Hi Ho', 'Arijit Singh'),
        ('7F8RNvTQlvbeBLeenycvN6', 'Kun Faya Kun', 'A.R. Rahman'),
        ('3jtKSUiVDowKNBqVQbWaig', 'Iktara', 'Amit Trivedi'),
        ('1UWacd8x8tPPwmrPB1MoBI', 'Ae Dil Hai Mushkil', 'Arijit Singh'),
        ('7cWnks0lsRtpAi87COOiXK', 'O Re Piya', 'Rahat Fateh Ali Khan'),
    ],
    'surprise': [
        ('7ltsfuHdqTZ5LwPpDy1q0v', 'Chaiyya Chaiyya', 'Sukhwinder Singh'),
        ('4i3MgUew8ynhf49Qwr4IP4', 'Jai Ho', 'A.R. Rahman'),
        ('1MCpLhYiT4dzn0sUCjWX4b', 'Malhari', 'Vishal Dadlani'),
        ('4ila6GeGBPGmJTGRoHOV5E', 'Nagada Sang Dhol', 'Shreya Ghoshal'),
        ('0CtZpaOhtzvLV3FfcsVpQo', 'Besharam Rang', 'Vishal-Shekhar'),
    ],
}

# ─── Telugu (Tollywood) Tracks — Verified Spotify Track IDs ───────────────────
EMOTION_TRACKS_TELUGU = {
    'happy': [
        ('0dnDTvdUco2UbaBjUtPxNS', 'Buttabomma', 'Armaan Malik'),
        ('3j9DrRebdWK1jkpOw9FZUy', 'Samajavaragamana', 'Sid Sriram'),
        ('4iKGu3xtvm90eBw0EIPWJP', 'Naatu Naatu', 'Rahul Sipligunj'),
        ('7uUugUpLi9js1AwUusoZ1h', 'Inkem Inkem Inkem Kaavaale', 'Sid Sriram'),
        ('1bxzr3JK05fMTcweGAZUHp', 'Chuttamalle', 'Shilpa Rao'),
    ],
    'sad': [
        ('2LTgKIErzHLjtQjIEkGrU5', 'Adiga Adiga', 'Sid Sriram'),
        ('4Ua5t8kTLSnVKWV2NK2xiN', 'Vintunnava', 'A.R. Rahman'),
        ('1vnDu8pbmwz88G6RDugerQ', 'Kannuladha', 'Anirudh Ravichander'),
        ('3K8KLno4fDcBvBLiYAzVWf', 'Oosupodu', 'Hemachandra'),
        ('0aVRaPEpi5bXOrl85m22DP', 'Priyathama Priyathama', 'Chinmayi Sripada'),
    ],
    'angry': [
        ('0KQKewxcCrFf26B5pxR2hv', 'Seeti Maar', 'Thaman S'),
        ('2YmXGUx32C3CUEgcAyHcGf', 'Srivalli', 'Sid Sriram'),
        ('3qWfqpB8KJFxwvbpqbuLCh', 'Ramuloo Ramulaa', 'Anurag Kulkarni'),
        ('55HpW5wBY4LFazpiczHLFD', 'Jaragandi', 'Daler Mehndi'),
        ('4OmbwFpYB41rQZZUGGtFZZ', 'Jinthaak', 'Bheems Ceciroleo'),
    ],
    'fear': [
        ('48idlZoTeP4xi6ZHBoFbYy', 'Bhairava Anthem', 'Diljit Dosanjh'),
        ('5bnxMZqd9Kpn9ByHj3Dc9C', 'Pushpa Pushpa', 'Devi Sri Prasad'),
        ('2VJGtBxZjebKXIfeYquN3z', 'The Fear Song', 'Anirudh Ravichander'),
        ('3S2R0EVwBSAVMd5UMgKTL0', 'Thriller', 'Michael Jackson'),
        ('6CCV7FeYgEQ7Ekbes6B36Q', 'Bhool Bhulaiyaa', 'Neeraj Shridhar'),
    ],
    'disgust': [
        ('3szxldqiYs7nkvtmooRod8', 'Oo Antava', 'Indravathi Chauhan'),
        ('14mBPBlZFOUHbeWknssiTw', 'Thulli Thulli', 'Sujatha'),
        ('0bffLPVYVInU8luH7Wv1Pr', 'Blockbuster', 'S.S. Thaman'),
        ('2sHHVNvfUlegjyhJpRzJjX', 'Bewafa', 'Imran Khan'),
        ('5XeFesFbtLpXzIVDNQP22n', 'I Wanna Be Yours', 'Arctic Monkeys'),
    ],
    'neutral': [
        ('2RF0pXYxQz9LMYU4orM4Y6', 'Ee Snehame', 'Udit Narayan'),
        ('6g80HDTAxMCljlZXttTv3k', 'Manasuna Manasai', 'Vasanth G'),
        ('3rAgt4iGMiIEoqy8PDH5t6', 'Kalyana Vaibhogame', 'Kalyani Mallik'),
        ('76eCC3r9jrVDsQnfAqQNH4', 'Inthalo Ennenni Vinthalo', 'Naresh Iyer'),
        ('5ThyDv6aRVU8AH4vXQNldF', 'Finding Her', 'Family Star OST'),
    ],
    'surprise': [
        ('0UnR6MoFXU76naQSf7vPPW', 'Naatu Naatu Remix', 'Rahul Sipligunj'),
        ('55HpW5wBY4LFazpiczHLFD', 'Jaragandi', 'Daler Mehndi'),
        ('6EKYYYxJiDD40v6rg3pt07', 'Sooseki', 'Shreya Ghoshal'),
        ('7MB17pZvTfbLWAck4z4ZoV', 'Oh My Baby', 'Shilpa Rao'),
        ('4iKGu3xtvm90eBw0EIPWJP', 'Naatu Naatu', 'Rahul Sipligunj'),
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

# Keep EMOTION_PLAYLISTS as alias for backward compatibility
EMOTION_PLAYLISTS = {k: [f"track/{v[0][0]}" for v in [vals]] for k, vals in EMOTION_TRACKS.items()}

# Emotion-to-Color mapping for Adaptive UI
EMOTION_COLORS = {
    "angry":   "#FF4B2B",   # Deep Red
    "disgust": "#2ECC71",   # Emerald Green
    "fear":    "#9B59B6",   # Amethyst Purple
    "happy":   "#F1C40F",   # Sun Flower Yellow
    "neutral": "#60a5fa",   # Blue
    "sad":     "#3498DB",   # Bright Blue
    "surprise":"#E67E22"    # Carrot Orange
}

APP_TITLE    = "🎭 Live Mood Beats"
APP_SUBTITLE = "Real-time Emotion Prediction & Personalized Music"

COLOR_PALETTE = {
    "primary":    "#FF4B4B",
    "background": "#0E1117",
    "text":       "#FAFAFA",
    "accent":     "#1DB954"
}

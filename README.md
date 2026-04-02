# 🎭 Live Mood Beats

**Live Mood Beats** is a real-time emotion detection web application built with **TensorFlow**, **OpenCV**, and **Streamlit**. It analyzes your facial expressions via live webcam, photo, or video, and automatically plays a **Spotify** playlist that matches your mood.

## ✨ Features
- **📽️ Live Detection**: Real-time emotion tracking from your camera.
- **🖼️ Photo Upload**: Analyze static images (JPG, PNG).
- **🎬 Video Upload**: Extract the dominant mood from video clips.
- **🎧 Mood-Synced Music**: Seamlessly integrated Spotify playlists for each emotion.
- **🌈 Adaptive UI**: The application's theme and visuals change dynamically based on the detected emotion.

## 🚀 Deployment Instructions (Streamlit Cloud)
1. Fork or upload this repository to your **GitHub** account.
2. Visit [**share.streamlit.io**](https://share.streamlit.io/).
3. Connect your GitHub account and select this repository.
4. Set the main file to **`app.py`**.
5. Click **Deploy!**

## 🛠️ Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🧠 Model Information
Uses a pre-trained **FER2013** emotion detection model with 7 labels:
- Angry 
- Disgust
- Fear
- Happy
- Neutral
- Sad
- Surprise

---
*Created with visual excellence and powered by Streamlit.*

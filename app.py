# app.py
import streamlit as st
import random
import time
import cv2
import numpy as np
from PIL import Image
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, WebRtcMode

# Import our modular components
from src.config import APP_TITLE, APP_SUBTITLE, EMOTION_PLAYLISTS
from src.model_utils import load_emotion_model, predict_emotion
from src.styles import apply_styles
from src.video_processor import EmotionProcessor, result_queue

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# State Management
# -------------------------------
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "neutral"
if "playlist_url" not in st.session_state:
    st.session_state.playlist_url = random.choice(EMOTION_PLAYLISTS["neutral"])

# Apply adaptive aurora styles
apply_styles(st.session_state.last_emotion)

# -------------------------------
# Layout & Logo
# -------------------------------
st.markdown(f'<div class="mood-badge">{st.session_state.last_emotion}</div>', unsafe_allow_html=True)
st.title(APP_TITLE)
st.markdown(f"#### {APP_SUBTITLE}")

# -------------------------------
# Model Loading
# -------------------------------
with st.spinner("Synchronizing neural networks..."):
    model = load_emotion_model()

# -------------------------------
# Tabs for Different Modes
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📽️ Live Detection", "🖼️ Photo Upload", "🎬 Video Upload"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.8, 1.2], gap="large")

    with col1:
        st.markdown("### Live Stream")
        
        RTC_CONFIGURATION = RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )

        ctx = webrtc_streamer(
            key="emotion-detection",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            video_processor_factory=lambda: EmotionProcessor(model),
            media_stream_constraints={
                "video": {
                    "width": {"ideal": 1280},
                    "height": {"ideal": 720},
                    "frameRate": {"ideal": 30}
                }, 
                "audio": False
            },
            async_processing=True,
        )

    with col2:
        st.markdown("### 🎧 Harmony Pick")
        
        music_placeholder = st.empty()
        
        if ctx.state.playing:
            while True:
                new_emotion = None
                while not result_queue.empty():
                    new_emotion = result_queue.get()
                
                if new_emotion is not None and new_emotion != st.session_state.last_emotion:
                    st.session_state.last_emotion = new_emotion
                    st.session_state.playlist_url = random.choice(EMOTION_PLAYLISTS.get(new_emotion, EMOTION_PLAYLISTS["neutral"]))
                    st.rerun()
                    
                with music_placeholder.container():
                    st.markdown(f"#### Your {st.session_state.last_emotion.capitalize()} Mix:")
                    playlist_id = st.session_state.playlist_url.split("/")[-1]
                    st.markdown(f'<iframe src="https://open.spotify.com/embed/playlist/{playlist_id}" width="100%" height="450" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
                
                time.sleep(0.1)
                break
        else:
            st.markdown("##### Waiting for visual cues...")
            st.caption("Press 'Start' to begin the mood-synced experience.")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.8, 1.2], gap="large")
    
    with col1:
        st.markdown("### Image Analysis")
        uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            frame = np.array(image.convert('RGB'))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            with st.spinner("Analyzing your expression..."):
                emotion, confidence, processed_frame = predict_emotion(model, frame)
                
                # Update session state if emotion changes
                if emotion != st.session_state.last_emotion:
                    st.session_state.last_emotion = emotion
                    st.session_state.playlist_url = random.choice(EMOTION_PLAYLISTS.get(emotion, EMOTION_PLAYLISTS["neutral"]))
                    st.rerun()
                
                # Show processed image
                processed_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                st.image(processed_rgb, caption=f"Detected Emotion: {emotion.upper()} ({confidence:.2f})", use_container_width=True)
    
    with col2:
        st.markdown("### 🎧 Harmony Pick")
        st.markdown(f"#### Your {st.session_state.last_emotion.capitalize()} Mix:")
        playlist_id = st.session_state.playlist_url.split("/")[-1]
        st.markdown(f'<iframe src="https://open.spotify.com/embed/playlist/{playlist_id}" width="100%" height="450" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.8, 1.2], gap="large")
    
    with col1:
        st.markdown("### Video Analysis")
        uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "mov", "avi"])
        
        if uploaded_video is not None:
            # Temporary save since cv2 needs a file path
            import tempfile
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_video.read())
            
            cap = cv2.VideoCapture(tfile.name)
            st.info("Reading video frames and analyzing the most prominent mood...")
            
            # Simple logic: analyze first 30 frames or sample across the video
            emotions = []
            frames_to_check = 20
            ret, frame = cap.read()
            count = 0
            
            progress_bar = st.progress(0)
            while ret and count < frames_to_check:
                emotion, _, _ = predict_emotion(model, frame)
                emotions.append(emotion)
                count += 1
                progress_bar.progress(count / frames_to_check)
                ret, frame = cap.read()
            
            cap.release()
            
            if emotions:
                from statistics import mode
                final_emotion = mode(emotions)
                
                if final_emotion != st.session_state.last_emotion:
                    st.session_state.last_emotion = final_emotion
                    st.session_state.playlist_url = random.choice(EMOTION_PLAYLISTS.get(final_emotion, EMOTION_PLAYLISTS["neutral"]))
                    st.rerun()
                
                st.success(f"Dominant Mood Detected: {final_emotion.upper()}")
                st.video(uploaded_video)
    
    with col2:
        st.markdown("### 🎧 Harmony Pick")
        st.markdown(f"#### Your {st.session_state.last_emotion.capitalize()} Mix:")
        playlist_id = st.session_state.playlist_url.split("/")[-1]
        st.markdown(f'<iframe src="https://open.spotify.com/embed/playlist/{playlist_id}" width="100%" height="450" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)

# -------------------------------
# Footer
# -------------------------------
st.divider()
st.caption("Powered by TensorFlow & Streamlit • Created for visual excellence")


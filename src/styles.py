# src/styles.py
import streamlit as st
from src.config import EMOTION_COLORS

def apply_styles(current_emotion="neutral"):
    """Apply dynamic Adaptive Aurora styles based on the current emotion."""
    
    # Get the theme color for the current emotion
    accent_color = EMOTION_COLORS.get(current_emotion, "#60a5fa")
    
    # Create the dynamic CSS
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

        * {{
            font-family: 'Outfit', sans-serif;
        }}

        /* Main app background with Calm Dark Blue theme */
        .stApp {{
            background: #0a1128 !important; /* Deep Dark Blue */
        }}

        .stApp::before {{
            display: none !important; /* Disable radial pulse */
        }}

        /* Typography reboot */
        h1, h2, h3 {{
            color: white !important;
            font-weight: 800 !important;
            letter-spacing: -1px !important;
        }}

        h1 {{
            font-size: 3rem !important;
            margin-bottom: 0px !important;
            background: linear-gradient(to right, white, {accent_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* Premium Floating Containers */
        div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            margin-bottom: 24px;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* Buttons and Inputs */
        .stButton > button {{
            background: {accent_color} !important;
            color: #000 !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            border: none !important;
            box-shadow: 0 10px 20px {accent_color}33 !important;
            transition: all 0.3s ease !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 15px 30px {accent_color}55 !important;
        }}

        /* Hide standard elements */
        #MainMenu, footer, header {{ visibility: hidden; }}

        /* Custom mood indicator */
        .mood-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 100px;
            background: {accent_color}22;
            color: {accent_color};
            border: 1px solid {accent_color}44;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
            margin-bottom: 16px;
        }}

        /* Video styling */
        video {{
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        }}
        
        iframe {{
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        </style>
    """, unsafe_allow_html=True)

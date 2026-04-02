# src/model_utils.py
import os
import cv2
import numpy as np
import tensorflow as tf
import streamlit as st
from .config import EMOTION_LABELS

@st.cache_resource
def load_emotion_model():
    """Load the pre-trained Keras model."""
    model_path = "fer2013_emotion_model.h5"
    if not os.path.exists(model_path):
        # Fallback to copy if first one missing (based on list_dir results)
        model_path = "fer2013_emotion_model (1).h5"
    
    return tf.keras.models.load_model(model_path, compile=False)

def preprocess_frame(frame):
    """
    Preprocess a BGR frame for the grayscale model.
    1. Grayscale conversion
    2. Histogram Equalization (CLAHE) for lighting robustness
    3. Resize to 48x48
    4. Rescale by 1/255.0
    5. Expand dims
    """
    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)
    
    # Resize
    resized = cv2.resize(gray, (48, 48))
    
    # Cast to float32 and normalize
    img_array = resized.astype("float32") / 255.0
    
    # Expand dims for batching (1, 48, 48, 1)
    return np.expand_dims(img_array, axis=(0, -1))

def predict_emotion(model, frame):
    """
    Detect faces in the frame and predict emotion for the largest face.
    Returns (emotion_label, confidence, processed_frame)
    """
    # Load cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Tweak parameters for better detection in low light
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30))
    
    detected_emotion = "neutral"
    confidence = 0.0
    
    # Find the largest face
    if len(faces) > 0:
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        (x, y, w, h) = faces[0]
        
        # Draw rectangle
        # Using the accent color for the box (e.g. Blue/Green)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Crop and predict
        face_roi = frame[y:y+h, x:x+w]
        processed = preprocess_frame(face_roi)
        
        preds = model.predict(processed, verbose=0)
        max_idx = np.argmax(preds[0])
        detected_emotion = EMOTION_LABELS[max_idx]
        confidence = float(preds[0][max_idx])
        
        # Add label overlay
        label_text = f"{detected_emotion.upper()} ({confidence:.2f})"
        cv2.putText(frame, label_text, (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
    return detected_emotion, confidence, frame

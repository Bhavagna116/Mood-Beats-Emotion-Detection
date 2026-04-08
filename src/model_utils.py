# src/model_utils.py
import os
import cv2
import numpy as np
import tensorflow as tf
from .config import EMOTION_LABELS

def load_emotion_model():
    """Load the pre-trained Keras model."""
    model_path = "fer2013_emotion_model.h5"
    if not os.path.exists(model_path):
        # Fallback to copy if first one missing (based on list_dir results)
        model_path = "fer2013_emotion_model (1).h5"
    
    return tf.keras.models.load_model(model_path, compile=False)

def preprocess_frame(frame):
    """
    Preprocess a BGR frame exactly as the FER2013 training data.
    1. Grayscale conversion
    2. Resize to 48x48
    3. Rescale by 1/255.0
    4. Expand dims
    """
    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize directly without distorting contrast
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
    
    # If the frame is massively large (e.g., from a phone camera), shrink it down to prevent total server timeout
    if frame.shape[1] > 1000:
        scale_percent = 1000 / frame.shape[1]
        width = int(frame.shape[1] * scale_percent)
        height = int(frame.shape[0] * scale_percent)
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Reverting to safer scaleFactor to prevent 100% CPU lock or Render gateway timeouts on huge images
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
    
    detected_emotion = "neutral"
    confidence = 0.0
    
    # Find the largest face
    if len(faces) > 0:
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        (x, y, w, h) = faces[0]
        
        # Pad the bounding box by 10% to ensure chin and mouth (vital for 'sad'/'surprise') are included
        pad_w = int(w * 0.1)
        pad_h = int(h * 0.1)
        
        # Calculate new coordinates with bounds checking
        y1 = max(0, y - pad_h)
        y2 = min(frame.shape[0], y + h + pad_h)
        x1 = max(0, x - pad_w)
        x2 = min(frame.shape[1], x + w + pad_w)
        
        # Draw rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Crop and predict
        face_roi = frame[y1:y2, x1:x2]
        processed = preprocess_frame(face_roi)
        
        preds = model.predict(processed, verbose=0)[0]
        
        # FER2013 is heavily biased towards happy and neutral.
        # We apply an ADDITIVE bias to the raw probabilities to aggressively compensate
        # for the dataset's reluctance to output 'sad' or 'fear'.
        # Indexes: 0=angry, 1=disgust, 2=fear, 3=happy, 4=neutral, 5=sad, 6=surprise
        preds[5] += 0.35  # Massive additive boost for 'Sad'
        preds[2] += 0.20  # Boost 'Fear'
        preds[1] += 0.25  # Boost 'Disgust'
        preds[0] += 0.10  # Boost 'Angry' 
        
        # Mildly penalize Happy and Neutral to suppress false positives
        preds[3] = max(0.0, preds[3] - 0.15)
        preds[4] = max(0.0, preds[4] - 0.10)
        
        max_idx = np.argmax(preds)
        detected_emotion = EMOTION_LABELS[max_idx]
        confidence = float(preds[max_idx] / np.sum(preds)) # Recalculate normalized confidence
        
        # Add label overlay
        label_text = f"{detected_emotion.upper()} ({confidence:.2f})"
        cv2.putText(frame, label_text, (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
    return detected_emotion, confidence, frame

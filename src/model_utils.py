# src/model_utils.py
import os
import cv2
import numpy as np
import tensorflow as tf
from .config import EMOTION_LABELS

def load_emotion_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'fer2013_emotion_model.tflite')
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def preprocess_frame(frame):
    """
    Robust preprocessing for all 7 emotions including fear and disgust.
    Uses CLAHE histogram equalization to boost contrast for subtle expressions.
    """
    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # This significantly helps with fear/disgust which are low-contrast emotions
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Resize to 48x48 (FER2013 standard)
    resized = cv2.resize(gray, (48, 48), interpolation=cv2.INTER_LANCZOS4)

    # Normalize to [0, 1]
    img_array = resized.astype("float32") / 255.0

    # Expand dims for batching (1, 48, 48, 1)
    return np.expand_dims(img_array, axis=(0, -1))


def predict_emotion(model, frame):
    """
    Detect faces in the frame and predict emotion for the largest face.
    Returns (emotion_label, confidence, processed_frame)
    """
    detected_emotion = "neutral"
    confidence = 0.0

    try:
        # Load cascade for face detection
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Shrink large frames (mobile cameras) to prevent server timeout
        if frame.shape[1] > 1000:
            scale_percent = 1000 / frame.shape[1]
            width = int(frame.shape[1] * scale_percent)
            height = int(frame.shape[0] * scale_percent)
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

        # Convert to grayscale for detection; equalize for better face finding
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_eq = cv2.equalizeHist(gray)

        # Detect faces with slightly relaxed params to catch subtle expressions
        faces = face_cascade.detectMultiScale(
            gray_eq,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(28, 28),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) > 0:
            # Use the largest detected face
            faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
            (x, y, w, h) = faces[0]

            # Pad the bounding box by 15% to ensure forehead/chin are captured
            # (critical for surprise/fear/disgust where eyebrow/lip area matters)
            pad_w = int(w * 0.15)
            pad_h = int(h * 0.15)

            y1 = max(0, y - pad_h)
            y2 = min(frame.shape[0], y + h + pad_h)
            x1 = max(0, x - pad_w)
            x2 = min(frame.shape[1], x + w + pad_w)

            # Draw bounding rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Crop face ROI and preprocess
            face_roi = frame[y1:y2, x1:x2]
            processed = preprocess_frame(face_roi)

            input_details = model.get_input_details()
            output_details = model.get_output_details()

            model.set_tensor(input_details[0]['index'], processed)
            model.invoke()
            # Copy immediately to avoid TFLite internal reference RuntimeError
            raw_preds = model.get_tensor(output_details[0]['index']).copy()

            preds = np.array(raw_preds[0], dtype=np.float32)

            # Apply temperature scaling (T=0.7) to sharpen probability distribution
            # This makes the model more decisive and improves per-class accuracy
            temperature = 0.7
            preds = preds / temperature
            # Softmax
            preds = preds - np.max(preds)  # numerical stability
            preds = np.exp(preds)
            preds = preds / np.sum(preds)

            max_idx = np.argmax(preds)
            detected_emotion = EMOTION_LABELS[max_idx]
            confidence = float(preds[max_idx])

            # Draw label
            emotion_display = detected_emotion.upper()
            conf_pct = int(confidence * 100)
            label_text = f"{emotion_display} {conf_pct}%"
            cv2.putText(
                frame, label_text,
                (x1, max(0, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
            )

    except Exception as e:
        import traceback
        traceback.print_exc()

    return detected_emotion, confidence, frame

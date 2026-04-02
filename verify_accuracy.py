import cv2
import numpy as np
import tensorflow as tf
from src.model_utils import load_emotion_model, preprocess_frame
from src.config import EMOTION_LABELS

def verify():
    try:
        model = load_emotion_model()
        print(f"Model input shape: {model.input_shape}")
        
        image_path = r"C:\Users\bhava\.gemini\antigravity\brain\5cb50ed4-5ee6-40ba-89cd-ef46eb606b69\test_face_happy_1775112516828.png"
        
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Error: Could not load image {image_path}")
            return
        
        # Detection logic similar to live app
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            print("No faces detected.")
            # Fallback to whole image if no face detected for testing
            face_roi = frame
        else:
            x, y, w, h = faces[0]
            face_roi = frame[y:y+h, x:x+w]
        
        processed = preprocess_frame(face_roi)
        print(f"Processed shape: {processed.shape}")
        
        preds = model.predict(processed, verbose=0)
        max_idx = np.argmax(preds[0])
        label = EMOTION_LABELS[max_idx]
        confidence = float(preds[0][max_idx])
        
        print(f"Detected Label: {label}")
        print(f"Confidence: {confidence:.4f}")
        print("Probabilities:")
        for i, l in enumerate(EMOTION_LABELS):
            print(f"  {l}: {preds[0][i]:.4f}")

    except Exception as e:
        import traceback
        print("An error occurred:")
        traceback.print_exc()

if __name__ == "__main__":
    verify()
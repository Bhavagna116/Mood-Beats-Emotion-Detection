# src/video_processor.py
import queue
from streamlit_webrtc import VideoProcessorBase
from .model_utils import predict_emotion
from collections import deque
from statistics import mode

# Global queue to send the latest detected emotion back to the main app thread
result_queue = queue.Queue()

class EmotionProcessor(VideoProcessorBase):
    def __init__(self, model):
        self.model = model
        # Buffer for stabilizing predictions (last 15 frames)
        self.emotion_history = deque(maxlen=15)

    def recv(self, frame):
        """Processes each incoming video frame."""
        img = frame.to_ndarray(format="bgr24")
        
        # Predict emotion
        detected_emotion, confidence, processed_frame = predict_emotion(self.model, img)
        
        # Add to history for stabilization
        self.emotion_history.append(detected_emotion)
        
        # Only send to queue if we have enough data and it's stable
        if len(self.emotion_history) == self.emotion_history.maxlen:
            stable_emotion = mode(self.emotion_history)
            # Only put if the queue is empty to avoid backlog (low lag)
            if result_queue.empty():
                result_queue.put(stable_emotion)
        
        return frame.from_ndarray(processed_frame, format="bgr24")

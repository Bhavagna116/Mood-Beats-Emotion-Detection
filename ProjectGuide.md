# Real-time Facial Emotion Recognition and Music Recommendation

This guide provides the complete overview of the project in its newly refactored **offline-first** mode.

## 1. Requirements Fulfilled
- **OpenCV**: Face detection via Haarcascade.
- **CNN/Vision Transformer**: Uses a `fer2013_emotion_model.h5` Keras Convolutional Neural Network.
- **Dataset Support**: Pre-trained on FER-2013. Local CSV parsing.
- **Detect 6/7 emotions**: Recognizes Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise.
- **Offline Mode**: Uses a local CSV-based database instead of external Spotify APIs. 
- **User Feedback System**: "Like / Dislike" feature inside the UI that modifies local state data.

## 2. Full Code Architecture & Logic
The codebase operates via **Streamlit**:
- **app.py**: Central UI entry. Reads the `music_dataset.csv`, loads the Keras model, captures user webcam via `webrtc_streamer`.
- **src/model_utils.py**: Performs `cv2.CascadeClassifier` face detection, then crops, processes, and pushes the ROI to the CNN for emotion validation.
- **src/video_processor.py**: The WebRTC stream handles callbacks asynchronously and pushes data frames into a `result_queue` queue.
- **music_dataset.csv**: A locally generated file parsing songs to emotions (e.g., Happy -> "Walking on Sunshine").

## 3. Training Pipeline
*If you need to retrain or update the current H5 model:*
1. Acquire datasets: FER-2013 or OAHEGA.
2. Structure images into `/train` and `/val` folder categories based on emotion names.
3. Use Keras `ImageDataGenerator` for augmentations.
4. Model stack:
   - Several `Conv2D` layers using `relu` and Batch Normalization.
   - `MaxPooling2D` & `Dropout` for parameter reduction.
   - Flat layer -> Dense networks.
5. Compile with Adam optimizer and `categorical_crossentropy` loss. 
6. Generate `# fer2013_emotion_model.h5`.

## 4. UI Implementation Details
- Uses Streamlit's cache bindings for the model so it natively stays resident in memory.
- Uses `st.columns()` and HTML `div/iframe` templates to generate stunning, offline-compatible cards.
- Dark theme gradient integration (styled via CSS in `src/styles.py`).

## 5. Deployment Steps
To execute and publish offline:
1. Ensure your environment has the required dependencies:
   ```bash
    pip install -r requirements.txt
    pip install streamlit-webrtc opencv-python numpy tensorflow pandas
   ```
2. Run the application locally in the parent working directory:
   ```bash
   cd emotion
   streamlit run app.py
   ```
3. To package this entirely offline as an executable, you can use PyInstaller:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed --add-data "fer2013_emotion_model.h5;." --add-data "music_dataset.csv;." app.py
   ```
   **Important Note**: Packaging Streamlit correctly via PyInstaller requires extra environment hooks and a specific run script.

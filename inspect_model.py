import os
import sys
# Set logging level to error for tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np

def inspect():
    try:
        model_path = "fer2013_emotion_model.h5"
        if len(sys.argv) > 1:
            model_path = sys.argv[1]
            
        if not os.path.exists(model_path):
            print(f"Error: {model_path} not found.")
            return

        model = tf.keras.models.load_model(model_path, compile=False)
        print("--- Model Information ---")
        print(f"Model Path: {model_path}")
        
        # Input Layer Info
        input_layer = model.layers[0]
        print(f"Input Shape: {model.input_shape}")
        
        # Check first layer type
        print(f"First Layer: {input_layer.name} ({type(input_layer).__name__})")
        
        # Prediction check
        actual_input_shape = model.input_shape
        if isinstance(actual_input_shape, list):
            actual_input_shape = actual_input_shape[0]
        
        # Extract dimensions (ignoring batch size)
        h, w, c = actual_input_shape[1], actual_input_shape[2], actual_input_shape[3]
        print(f"Detected Dimensions: {h}x{w} with {c} channels")
        
        if c == 3:
            print("Conclusion: Model expects RGB (3-channel) input.")
        elif c == 1:
            print("Conclusion: Model expects Grayscale (1-channel) input.")
        else:
            print(f"Conclusion: Model expects {c} channels.")

        # Test prediction with correct shape
        dummy_input = np.zeros((1, h, w, c))
        preds = model.predict(dummy_input, verbose=0)
        print(f"Test Prediction successful. Output shape: {preds.shape}")

    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    inspect()

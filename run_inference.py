import tensorflow as tf
import numpy as np
from PIL import Image
import time

# Define the path to your TFLite model
model_path = "model.tflite"  # Replace with the path to your TFLite model

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']

# Define class labels based on your dataset
class_labels = ["Class1", "Class2", "Class3", "Class4", "Class5", "Class6"]

# Function to perform inference on an image
def perform_inference(image_path):
    # Load and preprocess the image
    image = Image.open(image_path)
    image = image.convert("RGB")
    image = image.resize((input_shape[1], input_shape[2]))
    image = np.array(image) / 255.0  # Normalize to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], image)

    # Run inference
    start_time = time.time()
    interpreter.invoke()
    end_time = time.time()

    # Get the output tensor
    output = interpreter.get_tensor(output_details[0]['index'])

    # Get the predicted class label
    predicted_label_index = np.argmax(output[0])
    predicted_label = class_labels[predicted_label_index]

    # Get the confidence level
    confidence = np.max(output[0])

    return predicted_label, confidence, end_time - start_time

# Example usage
image_path = "path_to_input_image.jpg"  # Replace with the path to your input image
predicted_label, confidence, inference_time = perform_inference(image_path)
print(f"Predicted Label: {predicted_label}")
print(f"Confidence: {confidence:.2f}")
print(f"Inference Time: {inference_time:.2f} seconds")

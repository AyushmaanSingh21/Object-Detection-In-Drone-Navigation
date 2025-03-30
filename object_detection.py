import cv2
import numpy as np
import tensorflow as tf

# Load Pretrained MobileNetV2 model for object detection
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# Labels for ImageNet classes
LABELS_PATH = tf.keras.applications.mobilenet.decode_predictions

# Start the drone camera (use 0 for webcam or specific video source)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame for MobileNetV2
    img = cv2.resize(frame, (224, 224))  # Resize to 224x224 (input size)
    img = np.expand_dims(img, axis=0)  # Expand dimensions for batch processing
    img = tf.keras.applications.mobilenet.preprocess_input(img)  # Normalize

    # Predict objects in the frame
    predictions = model.predict(img)
    decoded_preds = LABELS_PATH(predictions, top=3)[0]  # Top 3 predictions

    # Display Predictions
    for i, (imagenet_id, label, score) in enumerate(decoded_preds):
        text = f"{label}: {score:.2f}"
        cv2.putText(frame, text, (10, 30 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Drone Object Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

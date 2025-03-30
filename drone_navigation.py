from object_detection import detect_objects  # Import detection function
from harmony_search import harmony_search  # Import path optimizer

# Get detected obstacles from object detection model
detected_obstacles = detect_objects()

# Run Harmony Search for optimized navigation
optimized_path = harmony_search(detected_obstacles)

print("Optimized Flight Path:", optimized_path)

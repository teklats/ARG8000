import cv2
import numpy as np

# Constants for calibration
KNOWN_WIDTH = 23.0  # Known width of the object in cm (e.g., a book or phone)
KNOWN_DISTANCE = 30.0  # Known distance from the camera to the object in cm


# Function to calculate focal length
def calculate_focal_length(known_width, known_distance, perceived_width):
    return (perceived_width * known_distance) / known_width


# Function to calculate distance
def calculate_distance(known_width, focal_length, perceived_width):
    return (known_width * focal_length) / perceived_width


# Initialize the camera
cap = cv2.VideoCapture(0)  # Replace with the correct camera index (e.g., 0 or 1)
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Step 1: Calibrate the focal length
print("Calibration: Place an object with a known width at a known distance.")
print("Press C to calibrate.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from the camera.")
        break

    # Display the frame and ask for manual ROI selection
    cv2.imshow("Calibration Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # Press 'c' to capture and select the ROI
        x, y, w, h = cv2.selectROI("Calibration: Select the object", frame, showCrosshair=True)
        cv2.destroyWindow("Calibration: Select the object")
        focal_length = calculate_focal_length(KNOWN_WIDTH, KNOWN_DISTANCE, w)
        print(f"Calibrated Focal Length: {focal_length:.2f}")
        break
    elif key == ord('q'):  # Press 'q' to quit calibration
        cap.release()
        cv2.destroyAllWindows()
        exit()

cv2.destroyWindow("Calibration Frame")

# Step 2: Live video distance measurement
print("Starting live video distance measurement...")
print("Press s to start measurement.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from the camera.")
        break

    # Convert to grayscale (optional, for efficiency)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Manual ROI selection (press 's' to select ROI)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Press 's' to select a new object
        x, y, w, h = cv2.selectROI("Select Object", frame, showCrosshair=True)
        cv2.destroyWindow("Select Object")

    # If an object is detected (manual or pre-selected), calculate the distance
    if 'w' in locals():  # Ensure `w` exists (ROI width)
        perceived_width = w
        distance = calculate_distance(KNOWN_WIDTH, focal_length, perceived_width)

        # Draw the ROI and distance on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame with the distance overlay
    cv2.imshow("Distance Measurement", frame)

    # Exit on 'q'
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
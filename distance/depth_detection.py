import cv2

# Constants for calibration
KNOWN_WIDTH = 14.0  # Average width of a human face in cm
KNOWN_DISTANCE = 50.0  # Distance from the camera in cm for calibration


# Function to calculate focal length
def calculate_focal_length(known_width, known_distance, perceived_width):
    return (perceived_width * known_distance) / known_width


# Function to calculate distance
def calculate_distance(known_width, focal_length, perceived_width):
    return (known_width * focal_length) / perceived_width


# Load pre-trained face detector (Haar cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haar-cascade_frontal-face_default.xml")

# Initialize the camera
cap = cv2.VideoCapture(0)  # Replace with your camera index
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Step 1: Calibrate focal length
print("Calibration: Place a face at a known distance from the camera.")
print("Press 'c' to calibrate.")
focal_length = None
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from the camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # Draw detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Calibration Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and len(faces) > 0:  # Press 'c' to capture and calculate focal length
        _, _, w, _ = faces[0]  # Use the first detected face
        focal_length = calculate_focal_length(KNOWN_WIDTH, KNOWN_DISTANCE, w)
        print(f"Calibrated Focal Length: {focal_length:.2f}")
        break
    elif key == ord('q'):  # Quit calibration
        cap.release()
        cv2.destroyAllWindows()
        exit()

cv2.destroyAllWindows()

# Step 2: Live distance measurement
print("Starting live video distance measurement...")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from the camera.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        # Calculate distance
        perceived_width = w
        distance = calculate_distance(KNOWN_WIDTH, focal_length, perceived_width)

        # Draw the bounding box and distance
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"Distance: {distance:.2f} cm", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Distance Measurement", frame)

    # Exit on 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import cloudinary
import cloudinary.uploader
import time
import serial
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("Cloud_Name"),
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("api_secret")
)

# Arduino serial port setup
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino port

# Function to add timestamp to the image
def add_timestamp(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image for timestamp addition")
        return

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 255, 0)  # Green
    thickness = 2
    margin = 10

    # Get the size of the image
    (text_width, text_height), _ = cv2.getTextSize(timestamp, font, font_scale, thickness)
    text_x = image.shape[1] - text_width - margin
    text_y = image.shape[0] - margin

    # Add the timestamp
    cv2.putText(image, timestamp, (text_x, text_y), font, font_scale, font_color, thickness)
    cv2.imwrite(image_path, image)

# Function to blur faces in the image
def blur_faces(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image for face blurring")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Blur each detected face
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.GaussianBlur(face, (99, 99), 30)
        image[y:y+h, x:x+w] = face

    cv2.imwrite(image_path, image)

# Function to upload image to Cloudinary
def upload_image(image_path, post_office_id):
    try:
        # Get the current timestamp
        timestamp = int(time.time())
        
        # Add more metadata, such as timestamp
        upload_result = cloudinary.uploader.upload(
            image_path,
            public_id=f"{post_office_id}_{timestamp}",
            context={
                "post_office_id": post_office_id,
                "timestamp": timestamp,
                "device": "Arduino Camera",
                "image_capture_time": time.ctime(timestamp)
            }
        )
        
        print(f"Image uploaded successfully: {upload_result['url']}")
        return True
    except Exception as e:
        print(f"Error uploading image: {e}")
        return False

# Function to capture image
def capture_image(image_path):
    cap = cv2.VideoCapture(0)  # Capture image from the first camera device
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(image_path, frame)  # Save the captured frame to the specified path
        print(f"Image captured: {image_path}")
    else:
        print("Error capturing image")
    cap.release()

# Main loop
while True:
    # Wait for request from Arduino
    if arduino.in_waiting > 0:
        request = arduino.readline().decode('utf-8').strip()
        
        # Check if the request is to upload an image
        if "REQUEST_IMAGE_UPLOAD" in request:
            try:
                # Extract the Post Office ID from the request
                post_office_id = request.split(":")[1]
                print(f"Received request for Post Office ID: {post_office_id}")
            except IndexError:
                print("Invalid request format")
                continue

            # Capture the image
            image_path = "captured_image.jpg"  # You can specify any path
            capture_image(image_path)

            # Add timestamp and blur faces
            add_timestamp(image_path)
            blur_faces(image_path)

            # Upload the image
            if upload_image(image_path, post_office_id):
                # Notify Arduino of the success
                arduino.write(b"UPLOAD_SUCCESS\n")
                print("Notified Arduino: UPLOAD_SUCCESS")
            else:
                # Notify Arduino of failure
                arduino.write(b"UPLOAD_FAILED\n")
                print("Notified Arduino: UPLOAD_FAILED")

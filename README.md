# Swachhta IoT Integration

This repository contains the IoT integration module for the Swachhta project. It combines IoT devices and software to monitor, analyze, and improve cleanliness and waste management processes.

---

## Features

- **IoT Device Integration**: Arduino-based setup for real-time data collection.
- **Image Capture and Processing**: Automated image capture and analysis.
- **Cloud Storage**: Captured images are securely saved in Cloudinary for easy access and management.
- **Environmental Monitoring**: Tracks cleanliness and waste levels using sensors.
- **RESTful APIs**: Facilitates communication between devices and backend systems.
- **Modular Design**: Easy to add or modify features.

---

## Technologies Used

- **Programming Language**: Python (Flask Framework)
- **IoT Hardware**: Arduino-compatible microcontrollers and sensors
- **Image Storage**: Cloudinary for saving and managing captured images
- **Environment Management**: `.env` file for configuration
- **Image Processing**: Integrated with OpenCV for analysis
- **Dependencies**: Managed using `requirements.txt`

---

## Project Structure

```plaintext
Swachhta-Iot-Integration/
│
├── arduino_code/            # Code for Arduino-based IoT devices
│   └── device_code.ino      # Example Arduino code
│
├── myenv/                   # Virtual environment directory (local setup)
│
├── .env                     # Configuration file for environment variables
├── app.py                   # Main application logic
├── captured_image.jpg       # Sample captured image for processing
├── requirements.txt         # List of Python dependencies
├── README.md                # Project documentation
```

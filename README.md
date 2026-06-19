# ESP32-S3 Cam Object Detection System with YOLO & Hardware Feedback

## Description
This is an advanced Computer Vision and Edge AI project that integrates an **ESP32-S3 CAM** microcontroller with a customized **YOLO** neural network. The system captures frames via the camera, streams them to a client machine for real-time object detection, and triggers a physical hardware buzzer on the ESP32 module whenever a target object is identified.

## Key Features
* **Wireless Video Streaming:** Configured ESP32-S3 as a standalone Wi-Fi Access Point hosting a lightweight HTTP server to stream JPEG frames.
* **YOLO Object Detection:** Implemented real-time object detection via Python using the Ultralytics YOLO framework with a confidence threshold optimization.
* **Hardware Feedback Loop:** Created an automated trigger system that sends HTTP requests back to the ESP32 to activate a hardware active buzzer using LEDC PWM control.
* **FPS Monitoring:** Real-time frames-per-second performance tracking displayed directly on the video feed.

## System Architecture
1. **ESP32-S3 CAM:** Captures video frames -> Serves them via `/capture` HTTP endpoint.
2. **Python Client:** Fetches frames -> Runs YOLO inference -> Displays results via OpenCV.
3. **Feedback:** If target detected -> Python calls `/buzz` on ESP32 -> Microcontroller activates the buzzer.

## Tech Stack
* **Hardware:** ESP32-S3 CAM, Active Buzzer.
* **Microcontroller Firmware:** C/C++ (Arduino IDE), ESP32 Camera Library, ESP HTTP Server.
* **Computer Vision Client:** Python 3, OpenCV, Ultralytics YOLO, Requests, NumPy.

## How to Run

### 1. Firmware Setup
* Open the code inside the `esp32_firmware` folder using Arduino IDE.
* Configure your board settings for **ESP32S3 Dev Module** (ensure PSRAM is enabled).
* Flash the code and open the Serial Monitor to check the local IP address.

### 2. Python Client Setup
* Install required packages: `pip install opencv-python numpy requests ultralytics`
* Update the `ESP32_IP` and `model_path` variables inside the script in the `python_detection` folder.
* Run the Python script: `python detector.py`

import cv2
import numpy as np
import requests
import time
from ultralytics import YOLO

# ================== SETTINGS ==================
# Enter the IP address of your ESP32 (visible in Arduino Serial Monitor)
ESP32_IP = "YOUR_ESP32_IP"  # Example: "192.168.4.1"
URL = f"http://{ESP32_IP}/capture"
BUZZ_URL = f"http://{ESP32_IP}/buzz"

MODEL_PATH = r"YOUR_MODEL_PATH"  # Example: "D:\Projects\best.pt"
CONF_THRESHOLD = 0.60
IMG_SIZE = 320  # Smaller means faster (320 or 416)
last_buzz_time = 0  # Cooldown timer for the buzzer
# =================================================

# Load the YOLO model
try:
    model = YOLO(MODEL_PATH)
    model.to('cpu')
    print("✅ YOLO model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit()

print(f"📡 Connecting to camera: {URL}")

while True:
    try:
        # 1. Fetch frame from ESP32
        img_resp = requests.get(URL, timeout=2)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        if frame is None:
            continue

        start_time = time.time()

        # 2. Object Detection (YOLO)
        results = model(frame, conf=CONF_THRESHOLD, imgsz=IMG_SIZE, verbose=False)[0]

        detected = False
        for box in results.boxes:
            detected = True
            # Draw bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"YOUR_OBJECT_NAME {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 3. Buzzer feedback logic (triggers if object found and 2+ seconds passed)
        if detected and (time.time() - last_buzz_time > 2):
            try:
                requests.get(BUZZ_URL, timeout=0.5)
                last_buzz_time = time.time()
                print("🔔 Object detected! Buzzer triggered!")
            except:
                pass

        # Calculate FPS
        fps = 1.0 / (time.time() - start_time)
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Display the video feed
        cv2.imshow("ESP32-S3 YOLO Detection", frame)

    except Exception as e:
        print(f"⌛ Waiting for camera or error occurred: {e}")
        time.sleep(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
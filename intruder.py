# intruder.py

import cv2
import datetime
import os

def record_intruder_video():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Webcam not accessible!")
            return

        # Create a directory for saved videos
        os.makedirs("intruder_logs", exist_ok=True)

        # Filename with timestamp
        filename = datetime.datetime.now().strftime("intruder_logs/intruder_%Y%m%d_%H%M%S.avi")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

        print("[*] Recording intruder...")

        for _ in range(100):  # ~5 seconds at 20 FPS
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break

        cap.release()
        out.release()
        print(f"[*] Intruder video saved as: {filename}")

    except Exception as e:
        print("Failed to record intruder:", e)

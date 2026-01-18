import cv2
from ultralytics import YOLO

def main():
    # Load YOLOv8 nano model (fast & lightweight)
    model = YOLO("yolov8n.pt")

    # Open Logitech webcam (index may be 1 on laptop)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        # Run YOLO inference (person class = 0)
        results = model(frame, classes=[0], conf=0.5)

        # Draw detections
        annotated_frame = results[0].plot()

        cv2.imshow("Day 2 - Person Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

def main():
    # Load YOLOv8 nano model
    model = YOLO("yolov8n.pt")

    # Initialize DeepSORT tracker
    tracker = DeepSort(max_age=30)

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

        # Run YOLO detection (person only)
        results = model(frame, classes=[0], conf=0.5)

        detections = []

        # Convert YOLO output to DeepSORT format
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = float(box.conf[0])

                w = x2 - x1
                h = y2 - y1

                detections.append(
                    ([int(x1), int(y1), int(w), int(h)], conf, "person")
                )

        # Update tracker
        tracks = tracker.update_tracks(detections, frame=frame)

        # Draw tracked persons
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, w, h = map(int, track.to_ltrb())

            cv2.rectangle(frame, (l, t), (l + w, t + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"ID {track_id}",
                (l, t - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow("Day 3 - Person Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

import cv2
import mediapipe as mp
import time

def main():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    prev_head_y = None
    prev_time = None
    fall_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        status_text = "Normal"

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            # Head (nose) and hip landmarks
            head_y = landmarks[mp_pose.PoseLandmark.NOSE].y
            left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP].y
            right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y
            hip_y = (left_hip_y + right_hip_y) / 2

            current_time = time.time()

            if prev_head_y is not None:
                dy = head_y - prev_head_y
                dt = current_time - prev_time

                # Sudden downward movement
                if dy > 0.15 and dt < 0.5 and hip_y > 0.6:
                    fall_detected = True
                    status_text = "FALL DETECTED"

            prev_head_y = head_y
            prev_time = current_time

            mp_draw.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        if fall_detected:
            cv2.putText(
                frame,
                "⚠ FALL DETECTED",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                3
            )

        cv2.imshow("Day 5 - Fall Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

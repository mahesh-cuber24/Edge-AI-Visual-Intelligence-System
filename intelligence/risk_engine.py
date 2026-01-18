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

    cap = cv2.VideoCapture(r"C:\Users\Mahesh\Downloads\Fall_Detection_with_YOLOv7_Pose_Estimation_Demo_1080P.mp4")
    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    prev_head_y = None
    prev_time = None
    risk_score = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        current_time = time.time()
        risk_increment = 0.0

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            mp_draw.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
    )
            head_y = landmarks[mp_pose.PoseLandmark.NOSE].y
            left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP].y
            right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y
            hip_y = (left_hip_y + right_hip_y) / 2

            if prev_head_y is not None:
                dy = head_y - prev_head_y
                dt = current_time - prev_time

                # Risk factor 1: sudden downward motion
                if dy > 0.12 and dt < 0.5:
                    risk_increment += 0.4

                # Risk factor 2: low body posture
                if hip_y > 0.6:
                    risk_increment += 0.3

                # Risk factor 3: instability (fast motion)
                if abs(dy / dt) > 0.6:
                    risk_increment += 0.2

            prev_head_y = head_y
            prev_time = current_time

        # Update risk score
        risk_score += risk_increment
        risk_score *= 0.95   # decay over time
        risk_score = min(risk_score, 1.0)

        # Determine risk level
        if risk_score > 0.7:
            risk_text = "HIGH RISK"
            color = (0, 0, 255)
        elif risk_score > 0.4:
            risk_text = "MEDIUM RISK"
            color = (0, 165, 255)
        else:
            risk_text = "LOW RISK"
            color = (0, 255, 0)

        cv2.putText(
            frame,
            f"Risk: {risk_score:.2f} ({risk_text})",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2
        )

        cv2.imshow("Day 6 - Risk Engine", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

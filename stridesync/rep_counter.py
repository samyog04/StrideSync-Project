import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Utility function to calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)  # First point (hip)
    b = np.array(b)  # Middle point (knee)
    c = np.array(c)  # End point (ankle)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    return angle if angle <= 180 else 360 - angle

# Variables
counter = 0
stage = None  # "down" or "up"

# Open webcam
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates (right leg for squats)
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Calculate angle
            angle = calculate_angle(hip, knee, ankle)

            # Visualize angle
            cv2.putText(image, f'Knee Angle: {int(angle)}', (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Rep counting logic
            if angle < 90:
                stage = "down"
            if angle > 160 and stage == "down":
                stage = "up"
                counter += 1
                print(f"Rep Count: {counter}")

        except:
            pass

        # Display reps
        cv2.rectangle(image, (0, 0), (225, 100), (245, 117, 16), -1)
        cv2.putText(image, 'REPS', (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(image, str(counter),
                    (15, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

        # Draw pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Show the output
        cv2.imshow('StrideSync Rep Counter (Squats) - Press q to quit', image)

        # Break loop on 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

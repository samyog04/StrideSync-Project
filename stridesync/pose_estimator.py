import cv2
import mediapipe as mp
from posture_validator import validate_posture
from rep_counter import RepCounter
from workout_logger import log_workout  # Optional: if you want MySQL logging

# Setup MediaPipe pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Choose exercise type (for logging & posture logic)
exercise = "squat"  # You can switch to "pushup", "bicep_curl", etc.
username = "demo_user"  # You can fetch this from user input/UI later

# Initialize rep counter
rep_counter = RepCounter(exercise)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip & convert color
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Draw landmarks
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Validate posture
        is_good_posture = validate_posture(results.pose_landmarks, exercise)

        # Count reps
        rep_counter.update(results.pose_landmarks, is_good_posture)

        # Overlay data
        cv2.putText(frame, f"Reps: {rep_counter.reps}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"Posture: {'Good' if is_good_posture else 'Bad'}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if is_good_posture else (0, 0, 255), 2)

    cv2.imshow("Workout Tracker", frame)

    # Press 'q' to quit and save data
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Save to database (optional)
        log_workout(username, exercise, rep_counter.reps, rep_counter.good_posture_count)
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

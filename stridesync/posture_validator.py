def validate_posture(landmarks, exercise):
    if exercise == "squat":
        # Example: use hip and knee Y-values to validate squat depth
        left_hip_y = landmarks.landmark[23].y
        left_knee_y = landmarks.landmark[25].y

        # A basic heuristic: knee should be below hip (for squat)
        if left_knee_y > left_hip_y:
            return True
        else:
            return False
    else:
        # Placeholder for other exercises
        return True

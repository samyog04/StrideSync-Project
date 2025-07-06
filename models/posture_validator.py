def is_posture_correct(angles):
    return all(45 < angle < 160 for angle in angles.values())

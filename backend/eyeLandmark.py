# this class tracks and detects eye landmark using mediapipe
# outputs eye landmarks

import mediapipe as mp


class EyeLandmark:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.left_eye_indices = [362, 385, 387, 263, 373, 380]
        self.right_eye_indices = [33, 160, 158, 133, 153, 144]

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_eye_landmarks(self, frame, face_landmarks):
        # converting normalized coordinates to pixel coordinates
        h, w, _ = frame.shape
        left_eye_points = []
        right_eye_points = []

        for idx in self.left_eye_indices:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            left_eye_points.append((x, y))

        for idx in self.right_eye_indices:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            right_eye_points.append((x, y))

        return left_eye_points, right_eye_points





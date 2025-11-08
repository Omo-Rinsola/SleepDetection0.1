"""
wraps up the sleep detection logic
"""

import numpy as np
import cv2
from eyeLandmark import EyeLandmark
from earCalculator import EarCalculator
import time


class Detect:
    def __init__(self):
        self.eye_landmark = EyeLandmark()
        self.ear_calculator = EarCalculator()
        self.threshold = 0.2
        self.eyes_closed_start_time = None
        self.sleep_time_threshold = 1.0


    def detect(self, frame):
        if frame is None:
            print(" Warning: Received empty frame — skipping detection.")
            return "No frame received"
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.eye_landmark.face_mesh.process(frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye_points, right_eye_points = self.eye_landmark.get_eye_landmarks(frame, face_landmarks)

                # Calculate the eye aspect ratio (EAR)
                left_ear = self.ear_calculator.calculate_ear(left_eye_points)
                right_ear = self.ear_calculator.calculate_ear(right_eye_points)

                # calculate average EAR
                average = self.ear_calculator.average_ear(left_ear, right_ear)
                print(f"EAR: {average:.4f} | Threshold: {self.threshold}")

                # threshold
                if average < self.threshold:
                    # Eyes are closed

                    if self.eyes_closed_start_time is None:
                        # Eyes just closed - start the timer
                        self.eyes_closed_start_time = time.time()
                        print(" Eyes just closed - starting timer...")
                        return "awake"

                    else:
                        # Eyes have been closed for a while - check duration
                        time_closed = time.time() - self.eyes_closed_start_time
                        print(f"Eyes closed for {time_closed:.2f} seconds")

                        if time_closed >= self.sleep_time_threshold:
                            # Eyes closed long enough = SLEEPING
                            print(" Status: SLEEPING (eyes closed for 2+ seconds)")
                            return "sleeping"
                        else:
                            # Eyes closed but not long enough yet
                            print(f" Status: AWAKE (waiting... {self.sleep_time_threshold - time_closed:.1f}s left)")
                            return "awake"

                else:
                    if self.eyes_closed_start_time is not None:
                        print("👁️ Eyes opened - resetting timer")

                    self.eyes_closed_start_time = None
                    print("Status: AWAKE")
                    return "awake"

        # no face detected - reset timer
        self.eyes_closed_start_time = None
        return "no-face-detected"

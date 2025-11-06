"""
This code calculates the eye aspect ratio (EAR)
to determine the eye vertical and horizontal distances

"""
import numpy as np


class EarCalculator:
    def __init__(self):
        pass

    def calculate_ear(self, eye_points):
        # Vertical distances (height of eye at two different points)
        vertical_1 = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))  # |p2-p6|
        vertical_2 = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))  # |p3-p5|

        # Horizontal distance (width of eye)
        horizontal = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))  # |p1-p4|

        # Calculate EAR
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

        return ear

    def average_ear(self, left_ear, right_ear):
        avg_ear = (left_ear + right_ear) / 2.0
        return avg_ear

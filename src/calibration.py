import numpy as np
import cv2
import pickle

class Calibration:
    def __init__(self):
        self.homography = None
        self.points_file = "homography.pkl"

    def load_homography(self):
        try:
            with open(self.points_file, "rb") as f:
                self.homography = pickle.load(f)
                print("Homography loaded.")
        except FileNotFoundError:
            print("No homography found. Run calibration first.")

    def save_homography(self):
        with open(self.points_file, "wb") as f:
            pickle.dump(self.homography, f)
            print("Homography saved.")

    def calibrate(self, camera_points, wall_points):
        self.homography, status = cv2.findHomography(np.array(camera_points), np.array(wall_points))
        self.save_homography()
        return self.homography

    def map_point(self, camera_point):
        if self.homography is None:
            raise ValueError("Homography not computed")
        cam_pt = np.array([[camera_point]], dtype='float32')
        wall_pt = cv2.perspectiveTransform(cam_pt, self.homography)
        return wall_pt[0][0]

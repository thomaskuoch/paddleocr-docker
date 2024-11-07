import math
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage


def infer_angle(img_array) -> float:
    if not isinstance(img_array, np.ndarray):
        img_array = cv2.imread(img_array)
    # https://stackoverflow.com/questions/46731947/detect-angle-and-rotate-an-image-in-python
    img_gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(
        img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5
    )
    if lines is None or len(lines) == 0:
        return 0
    angles = []
    for [[x1, y1, x2, y2]] in lines:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    median_angle = np.median(angles)
    return median_angle


def rotate(img_array, angle: float):
    if isinstance(img_array, (str, Path)):
        img_array = cv2.imread(img_array)
    if angle % 360 != 0:
        img_array = ndimage.rotate(img_array, angle)
    return img_array

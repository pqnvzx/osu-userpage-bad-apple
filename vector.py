import json
import os

import cv2
import numpy as np
import svgwrite
from scipy.interpolate import splev, splprep
from skimage import measure

SRC_DIR = "frames"
DST_DIR = "vector_frames"
WIDTH = 580.765625
HEIGHT = 360

os.makedirs(DST_DIR, exist_ok=True)


def trace_contours(image_path):
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    gray = cv2.resize(gray, (int(WIDTH), int(HEIGHT)))

    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    segments = []

    for contour in measure.find_contours(binary, 0.3):
        points = contour.astype(int)

        if len(points) < 2:
            continue

        head, *tail = points
        segment = "M{},{}".format(head[1], head[0])

        for y, x in tail:
            segment += " L{},{}".format(x, y)

        segments.append(segment)

    return " ".join(segments)


def convert_all():
    for index, filename in enumerate(sorted(os.listdir(SRC_DIR))):
        if not filename.endswith(".png"):
            continue

        payload = {"path": trace_contours(os.path.join(SRC_DIR, filename))}
        target = os.path.join(DST_DIR, "frame_{:04d}.json".format(index))

        with open(target, "w") as handle:
            json.dump(payload, handle)

    print("done")


if __name__ == "__main__":
    convert_all()
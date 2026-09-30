import os
from pathlib import Path
import cv2

VIDEO_FILE = Path("video.mp4")
FRAMES_DIR = Path("frames")
FRAME_W = 640
FRAME_H = 360


def extract_frames():
    print("cutting")

    if not os.path.exists(FRAMES_DIR):
        os.makedirs(FRAMES_DIR)

    capture = cv2.VideoCapture(VIDEO_FILE)
    number = 0

    while capture.isOpened():
        ok, frame = capture.read()

        if not ok:
            break

        frame = cv2.resize(frame, (FRAME_W, FRAME_H))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        black = (
            (frame[:, :, 0] == 0)
            & (frame[:, :, 1] == 0)
            & (frame[:, :, 2] == 0)
        )
        frame[black] = [0, 0, 0, 0]

        cv2.imwrite(os.path.join(FRAMES_DIR, "{:04d}.png".format(number)), frame)
        number += 1

    capture.release()
    print("done")


extract_frames()
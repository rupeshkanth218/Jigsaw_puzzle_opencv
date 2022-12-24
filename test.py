import cv2
import os
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)


def read_images(dir_path):
    img_list = []
    files = os.listdir(dir_path)
    for file in files:
        img_path = os.path.join(dir_path, file)
        image = cv2.imread(img_path)
        img_list.append(image)

    return img_list


def draw_img(frame, img, x, y):
    w, h = img.shape[:2]
    frame[y:y + h, x:x + w] = img
    return frame


class Piece:

    def __init__(self, img, pos):
        self.img = img
        self.pos = pos

    def update_pos(self, new_pos):
        w, h = self.img.shape[:2]
        x, y = self.pos

        if x < new_pos[0] < x+w and y < new_pos[1] < y+h:
            self.pos = new_pos[0]-w//2, new_pos[1]-h//2



images = read_images("{}\\images".format(os.getcwd()))

image_list = random.sample(images, k=4)
pieces = []

for i in range(4):
    pieces.append(Piece(image_list[i], (0+(100*i), 0)))

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    hands, frame = detector.findHands(frame, draw=True)  # drawing all the hand points
    # hands= detector.findHands(img,draw=False)
    if hands:
        lmList = hands[0]['lmList']
        l, _, __ = detector.findDistance((lmList[8][0], lmList[8][1]), (lmList[12][0], lmList[12][1]), frame)

        if l < 50:
            index_position = lmList[8][:2]
            for piece in pieces:
                piece.update_pos(index_position)


    for piece in pieces:
        frame = draw_img(frame, piece.img, piece.pos[0], piece.pos[1])
    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
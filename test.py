import cv2
import os
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
dest_colors = [(50, 168, 82), (50, 115, 168), (87, 50, 168), (168, 50, 150), ]
dest_coords = [(100+120*x, 350) for x in range(4)]

def read_images(dir_path):
    img_list = {}
    files = os.listdir(dir_path)
    for idx, file in enumerate(files):
        img_path = os.path.join(dir_path, file)
        image = cv2.imread(img_path)
        img_list[idx+1] = image

    return img_list


def draw_img(cam_frame, img, x, y):
    w, h = img.shape[:2]
    cam_frame[y:y + h, x:x + w] = img
    return cam_frame


class Piece:

    def __init__(self, img, pos, value):
        self.img = img
        self.pos = pos
        self.value = value
        self.rank = None


    def update_pos(self, new_pos):
        w, h = self.img.shape[:2]
        x, y = self.pos

        if x < new_pos[0] < x+w and y < new_pos[1] < y+h:
            self.pos = new_pos[0]-w//2, new_pos[1]-h//2

    def set_rank(self, pics):
        self.rank = pics.index(self) + 1


images = read_images("{}\\images".format(os.getcwd()))

image_list = random.sample(list(images.keys()), k=4)
pieces = []

for i in range(4):
    pieces.append(Piece(images[image_list[i]], (0+(100*i), 0), image_list[i]))
for piece in pieces:
    piece.set_rank(pieces)

print([piece.rank for piece in pieces])
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # hands, frame = detector.findHands(frame, draw=True)  # drawing all the hand points
    hands= detector.findHands(frame, draw=False)
    if hands:
        lmList = hands[0]['lmList']
        l, _ = detector.findDistance((lmList[8][0], lmList[8][1]), (lmList[12][0], lmList[12][1]))

        if l < 50:
            index_position = lmList[8][:2]
            for piece in pieces:
                piece.update_pos(index_position)

    for piece in pieces:
        frame = draw_img(frame, piece.img, piece.pos[0], piece.pos[1])

    for x, color in zip(dest_coords, dest_colors):
        cv2.circle(frame, x, 5, color, 4)
    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import os
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
dest_colors = [(50, 168, 82), (50, 115, 168), (87, 50, 168), (168, 50, 150), ]
dest_coords = [(100+120*x, 250) for x in range(4)]
dest_coords = [(70, 200), (170, 200), (70, 300), (170, 300)]

start_img = cv2.imread("start.png")
end_img = cv2.imread("end.png")
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
    if x > -1 and y > -1:
        cam_frame[y:y + h, x:x + w] = img

    # print(cam_frame.shape, img.shape, x, y, w, h)
    return cam_frame


def set_rank(pic_obj ,some_pts):
    pics = pic_obj.copy()
    pics.sort(reverse=False, key=lambda x: x.value)
    for i, pic in enumerate(pics):
        pic.set_rank(i, some_pts)


class Piece:

    def __init__(self, img, pos, value):
        self.img = img
        self.pos = pos
        self.value = value
        self.rank = None
        self.final_pos = None
        self.reached=False

    def set_dest(self, dest_pts):
        self.final_pos = dest_pts[self.rank]

    def update_pos(self, new_pos):
        w, h = self.img.shape[:2]
        x, y = self.pos
        if x < new_pos[0] < x + w and y < new_pos[1] < y + h:
            if self.reached:
                self.pos = self.final_pos[0], self.final_pos[1]
            else:
                self.pos = new_pos[0] - w // 2, new_pos[1] - h // 2
        if abs(self.final_pos[0]-self.pos[0]) < 20 and abs(self.final_pos[1]-self.pos[1]) < 20:
            self.reached = True

    def set_rank(self, r, dest_pts):
        self.rank = r
        self.set_dest(dest_pts)

images = read_images("{}\\pieces".format(os.getcwd()))

image_list = random.sample(list(images.keys()), k=4)
pieces = []

for i in range(4):
    pieces.append(Piece(images[image_list[i]], (0+(110*i), 0), image_list[i]))

set_rank(pieces, dest_coords)
cv2.imshow("Webcam",start_img)
while cv2.waitKey(1) != ord(" "):
    cv2.waitKey(1)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # hands, frame = detector.findHands(frame, draw=True)  # drawing all the hand points
    hands = detector.findHands(frame, draw=False)
    if hands:
        lmList = hands[0]['lmList']
        l, _ = detector.findDistance((lmList[8][0], lmList[8][1]), (lmList[12][0], lmList[12][1]))

        if l < 50:
            index_position = lmList[8][:2]
            for piece in pieces:
                piece.update_pos(index_position)
    done = 0
    for piece in pieces:
        frame = draw_img(frame, piece.img, piece.pos[0], piece.pos[1])
        if piece.reached:
            done += 1
    for x, color in zip(dest_coords, dest_colors):
        cv2.circle(frame, x, 5, color, 4)
    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) == ord('q'):
        break
    if done == 4:

        cv2.waitKey(500)
        cv2.imshow("Webcam", end_img)
        cv2.waitKey(5000)
        break

cap.release()
cv2.destroyAllWindows()

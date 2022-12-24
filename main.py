from PIL import Image
import cv2
import os
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

def jigsaw_creator(img, row, col):
    # row -- how many cuts to make row wise
    # col -- how many cuts to make column wise
    w = img.width // col
    h = img.height // row
    x1, y1, x2, y2 = 0, 0, w, h
    count = 1
    for j in range(row):
        for i in range(col):
            img2 = img.crop(box=(x1 + (i * 90), y1 + (j * 90), x2 + (i * 90), y2 + (j * 90)))
            img2.save("images/img{}.png".format(count))
            count += 1


def read_images(dir_path):
    img_list = []
    files = os.listdir(dir_path)
    for file in files:
        img_path = os.path.join(dir_path, file)
        image = cv2.imread(img_path)
        img_list.append(image)

    return img_list


images = read_images("{}\\images".format(os.getcwd()))

# create mask of one of the image because mask will be same size as for all images

image_list = random.sample(images, k=4)
print(len(image_list))
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    hands, frame = detector.findHands(frame, draw=True)  # drawing all the hand points
    # hands= detector.findHands(img,draw=False)

    # region of interest
    for i in range(1, 5):
        img = image_list[i-1]
        w, h = img.shape[:2]

        # offset is the distance from the wall
        offset = 10
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)
        roi = frame[(-w)*i-offset:(-w)*(i-1)-offset, -h-offset:-offset]

        roi[np.where(mask)] = 0
        roi += img

    cv2.imshow('Webcam', frame)
    cv2.imshow("mask",mask)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()





#!/usr/bin/env python
import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

def findCCC(img):

    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,51,0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    imOpen = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    imClose = cv2.morphologyEx(imOpen, cv2.MORPH_CLOSE, kernel)

    im2, contours, hierarchy = cv2.findContours(imClose,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    targets = []

    for i in range(len(contours)):
        i2 = hierarchy[0][i][2]
        if i2 < 0:
            continue

        mu1 = cv2.moments(contours[i])
        x1 = np.array([mu1['m10']/mu1['m00'],mu1['m01']/mu1['m00']])
        mu2 = cv2.moments(contours[i2])
        x2 = np.array([mu2['m10']/mu2['m00'],mu2['m01']/mu2['m00']])

        if np.linalg.norm(np.subtract(x1,x2)) > 3:
            continue

        p = cv2.arcLength(contours[i], True)
        a = cv2.contourArea(contours[i])
        if 4*np.pi*a/(p*p) < np.pi/4:
            continue
        targets.append(x1)

    for i in range(len(targets)):
        x = int(targets[i][0])
        y = int(targets[i][1])
        cv2.circle(img, (x,y), 10, (0,0,255), 3)

    cv2.imshow('ccc', img)
    cv2.waitKey(20)

    # plt.subplot(2,2,1),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.title('Original'), plt.xticks([]), plt.yticks([])
    # plt.subplot(2,2,2),plt.imshow(im2)
    # plt.title('Circles'), plt.xticks([]), plt.yticks([])
    # plt.subplot(2,2,3),plt.imshow(imOpen)
    # plt.title('Edges'), plt.xticks([]), plt.yticks([])
    # plt.subplot(2,2,4),plt.imshow(imClose)
    # plt.title('Edges'), plt.xticks([]), plt.yticks([])
    #
    # mng = plt.get_current_fig_manager()
    # mng.resize(*mng.window.maxsize())
    #
    # plt.show()

def main():
    cap = cv2.VideoCapture(filename)
    if (not cap.isOpened()):
        print("Error opening video file")

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            findCCC(frame)
        else:
            break
    # for i in range(1):
    #     ret, frame = cap.read()
    # findCCC(frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt
import math

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

def distance(P, Q):
    return math.sqrt((P[0]-Q[0])**2 + (P[1]-Q[1])**2)

def findCode(img):
    image = img.copy()
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,51,0)

    edges = cv2.Canny(thresh,100,200)

    imCnt, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    imColor = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    # cv2.drawContours(imColor, contours, -1, (255,0,0), 1)

    markers = []
    for i in range(len(contours)):
        k = i
        c = 0
        while hierarchy[0][k][2] != -1:
            k = hierarchy[0][k][2]
            c += 1
        if hierarchy[0][k][2] != -1:
            c +=1
        if c >= 5:
            print c
            markers.append(i)

    mc = []
    for i in markers:
        mu = cv2.moments(contours[i])
        mc.append([mu['m10']/mu['m00'],mu['m01']/mu['m00']])
        print [mu['m10']/mu['m00'],mu['m01']/mu['m00']]

    corner = markers[0]
    if len(markers) == 3:
        d01 = distance(mc[0], mc[1])
        d12 = distance(mc[1], mc[2])
        d20 = distance(mc[2], mc[0])
        print d01
        print d12
        print d20

        if d01 > d12 and d01 > d20:
            corner = markers[2]
        elif d12 > d01 and d12 > d20:
            corner = markers[0]
        elif d20 > d01 and d20 > d12:
            corner = markers [1]


    for i in markers:
        cv2.drawContours(imColor, [contours[i]], 0, (255,0,0), 3)
        cv2.drawContours(imColor, [contours[corner]], 0, (0,255,0), 3)

    plt.subplot(2,2,1),plt.imshow(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,2),plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR))
    plt.title('Thresh'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,3),plt.imshow(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))
    plt.title('Img'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,4),plt.imshow(imColor)
    plt.title('Output'), plt.xticks([]), plt.yticks([])

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

    return imColor

def main():
    img = cv2.imread(filename,0)

    img = findCode(img)

    # cv2.imshow('qr',img)
    # cv2.waitKey(5000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

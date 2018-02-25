#!/usr/bin/env python
import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt
import math

class Cells(object):
    def __init__(self, image):
        print "Extracting cells"
        self.cells = self.removeLines(image)

    def removeLines(self, img):
        dst = cv2.Canny(img, 50, 200, None, 3)
        lines = cv2.HoughLines(dst, 1, np.pi/180, 120, None, 30, 10)
        cdst = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(cdst, pt1, pt2, (0,0,0), 10, cv2.LINE_AA)
        cdst = self.extractDigits(cdst)
        return cdst

    def extractDigits(self, img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imCnt, contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cdst = cv2.cvtColor(imgray, cv2.COLOR_GRAY2BGR)
        # cv2.drawContours(cdst, contours, -1, (255,0,0), 5)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(cdst, (x,y), (x+w,y+h), (255,0,0), 10)
            # cv2.drawContours(cdst, [cnt], 0, (255,0,0), 10)
            digit = cdst[y:y+h, x:x+w]
            # cv2.imshow("digit", digit)
            # cv2.waitKey(2000)
        return cdst

    def findCells(self, img):
        image = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        cells = []
        w,h = img.shape
        cell_w = w/9
        cell_h = h/9
        i,j = 0,0
        for r in range(0,w,cell_w):
            row = []
            j = 0
            for c in range(0,h,cell_h):
                cell = img[r:r+cell_w, c:c+cell_h]
                cell = cv2.resize(cell, (28,28))
                cv2.rectangle(image, (r,c), (r+cell_w, c+cell_h), (0,0,255), 2)

        # imColor = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
        # cv2.drawContours(imColor, [maxContour], 0, (255,0,0), imColor.shape[0]/50)
        # for i in rect:
        #     cv2.circle(imColor, (i[0],i[1]), 10, (0,0,255), -1)

        # plt.subplot(2,2,1),plt.imshow(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))
        # plt.title('Original'), plt.xticks([]), plt.yticks([])
        # plt.subplot(2,2,2),plt.imshow(cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR))
        # plt.title('Crop'), plt.xticks([]), plt.yticks([])
        # plt.subplot(2,2,3),plt.imshow(cv2.cvtColor(square, cv2.COLOR_GRAY2BGR))
        # plt.title('Img'), plt.xticks([]), plt.yticks([])
        # plt.subplot(2,2,4),plt.imshow(imColor)
        # plt.title('Output'), plt.xticks([]), plt.yticks([])
        #
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())
        # plt.show()

        return image

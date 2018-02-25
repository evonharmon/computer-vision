#!/usr/bin/env python
import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt
import math

class Extractor(object):
    def __init__(self, image):
        print "Extracting sudoku"
        self.sudoku = self.findCode(image)

    def preprocess(self, img):
        blur = cv2.GaussianBlur(img, (11,11), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,2)
        thresh = cv2.bitwise_not(thresh)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        # imopen = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        dilate = cv2.dilate(close, kernel)
        return dilate

    def findBorder(self, img):
        imCnt, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for cnt in contours[:min(5,len(contours))]:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.01*peri, True)
            if len(approx) == 4:
                return cnt
        return None

    def cropSudoku(self, img):
        maxContour = self.findBorder(img)
        x,y,w,h = cv2.boundingRect(maxContour)
        crop = img[y:y+h, x:x+w]
        square = cv2.resize(crop, (min(crop.shape), min(crop.shape)))
        return square

    def getCorners(self, cnt):
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt,0.01*peri, True)

        pts = approx.reshape(4,2)
        rect = np.zeros((4,2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts,axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def straighten(self, img, rect):
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warp = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
        return warp

    def findCode(self, img):
        image = img.copy()

        img = self.preprocess(img)

        crop = self.cropSudoku(img)

        maxContour = self.findBorder(crop)
        rect = self.getCorners(maxContour)
        square = self.straighten(crop, rect)

        imColor = cv2.cvtColor(crop,cv2.COLOR_GRAY2BGR)
        cv2.drawContours(imColor, [maxContour], 0, (255,0,0), imColor.shape[0]/50)
        for i in rect:
            cv2.circle(imColor, (i[0],i[1]), 10, (0,0,255), -1)

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

        return square

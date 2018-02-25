#!/usr/bin/env python
import numpy as np
import cv2 as cv

w = 600
h = 600
n = 8

def main():
    img = np.zeros((w,h,3), np.uint8)
    c = 0

    for i in range(n):
        for j in range(n):
            x1 = w/n*i
            x2 = w/n*(i+1)
            y1 = h/n*j
            y2 = h/n*(j+1)
            if not c:
                color = (0,0,0)
            else:
                color = (255,255,255)
            cv.rectangle(img,(x1,y1),(x2,y2),color,-1)
            c = not c
        c = not c

    cv.imshow('image',img)
    cv.waitKey(5000)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

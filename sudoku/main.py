#!/usr/bin/env python
import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt
import math
from extractor import Extractor
from cells import Cells

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

def main():
    image = cv2.imread(filename, 0)
    sudoku = Extractor(image).sudoku
    cells = Cells(sudoku).cells
    cv2.imshow('image', cells)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

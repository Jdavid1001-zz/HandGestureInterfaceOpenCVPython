# -*- coding: utf-8 -*-

import cv2
import numpy as np

def FrameToSkin(frame, lower, upper):
    #Flip frame to make into mirror
    frame = cv2.flip(frame, 1)
    #Convert to HSV
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Return mask for those within upper and lower range
    skinMask = cv2.inRange(converted, lower, upper)
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    # apply a series of erosions and dilations to the mask
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(frame, frame, mask = skinMask)
    return skin

def DiffSkin(skin1, skin2):
    grayskin1 = cv2.cvtColor(skin1, cv2.COLOR_BGR2GRAY)
    grayskin2 = cv2.cvtColor(skin2, cv2.COLOR_BGR2GRAY)
    skindiff = np.subtract(grayskin1, grayskin2)
    skindiff = np.absolute(skindiff)
    ret, thresh = cv2.threshold(skindiff, 100, 255, cv2.THRESH_BINARY)
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    # apply a series of erosions and dilations to the mask
    thresh = cv2.erode(thresh, kernel, iterations = 2)
    thresh = cv2.dilate(thresh, kernel, iterations = 2)
    return thresh
# -*- coding: utf-8 -*-
# import the necessary packages
#from pyimagesearch import imutils
import numpy as np
import argparse
import cv2
import SkinDetectionFunct as SDF



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())
 
# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")


# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, load the video
else:
	camera = cv2.VideoCapture(args["video"])
 
 
# keep looping over the frames in the video
(grabbed, frame) = camera.read()
fgbg = cv2.BackgroundSubtractorMOG2()
#fgbg.setDetectShadows(False)
#fgbg.setNMixtures(3)

foundHandSkin = False
frameNum = 0


if (args.get("video") and grabbed) or not args.get("video"):
    skin1 = SDF.FrameToSkin(frame, lower, upper)
    while True:
        (grabbed, frame2) = camera.read()
        newSkinBG = fgbg.apply(skin1)
        # if we are viewing a video and we did not grab a
        # frame, then we have reached the end of the video
        if args.get("video") and not grabbed:
            break
        skin2 = SDF.FrameToSkin(frame2, lower,upper)
        #Returns the highlighted difference between skin frames
        skindiff = SDF.DiffSkin(skin1, skin2)
        newskindiff = np.copy(skindiff)
        contours, hierarchy = cv2.findContours(newskindiff,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if not foundHandSkin and frameNum > 25:
            print "Doing this"
            #Returns the highlighted difference between skin frames
            Area = np.where(skindiff == 255)
            if len(Area[0]) >= 150:
                print "Now THis"
                foundHandSkin = True
                cnt = contours[0]
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                print cx, cy
                print skin2.shape
                newboundary = skin1[cy,cx]
                lowerS = newboundary[1] - 60
                higherS = newboundary[1] + 60
                lowerV = newboundary[2] - 60
                higherV = newboundary[2] + 60
                
                lower = np.array([0, SDF.round28bit(lowerS), SDF.round28bit(lowerV) ], dtype = "uint8")
                upper = np.array([20, SDF.round28bit(higherS), SDF.round28bit(higherV)], dtype = "uint8")
                print lower
                print upper
                """
                print skinPix.shape
                H,S,V = zip(*skinPix)
                hAvg = sum(H)/len(H)
                sAvg = sum(S)/len(S)
                vAvg = sum(V)/len(V)
                print hAvg
                print sAvg
                print vAvg
                lower = np.array([0, sAvg - 25, vAvg - 25], dtype = "uint8")
                print lower
                upper = np.array([20, sAvg + 25, vAvg + 25], dtype = "uint8")
                print upper"""
        #cv2.imshow("skindiff", skindiff)
        newSkin = np.copy(skin2)
        cv2.drawContours(newSkin, contours, -1, (0,255,0), 3)
        cv2.imshow("skindiff", skindiff)
        cv2.imshow("skin", newSkin)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        newSkinBG = cv2.dilate(newSkinBG, kernel, iterations = 2)
        cv2.imshow("newImages", newSkinBG)
        skin1 = np.copy(skin2)
        	# if the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        frameNum += 1
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


"""
        if not foundHandSkin and frameNum > 2:
            #Returns the highlighted difference between skin frames
            skindiff = SDF.DiffSkin(skin1, skin2)
            Area = np.where(skindiff == 255)
            cv2.imshow("skindiff", skindiff)
            if len(Area[0]) >= 150:
                foundHandSkin = True
                skinPix = np.copy(skin1[Area])
                print skinPix.shape
                H,S,V = zip(*skinPix)
                hAvg = sum(H)/len(H)
                sAvg = sum(S)/len(S)
                vAvg = sum(V)/len(V)
                print hAvg
                print sAvg
                print vAvg
                lower = np.array([hAvg-10, sAvg - 50, vAvg - 50], dtype = "uint8")
                print lower
                upper = np.array([hAvg+10, sAvg + 50, vAvg + 50], dtype = "uint8")
                print upper
                """








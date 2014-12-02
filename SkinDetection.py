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
if (args.get("video") and grabbed) or not args.get("video"):
    skin1 = SDF.FrameToSkin(frame, lower, upper)
    while True:
        (grabbed, frame2) = camera.read()
        # if we are viewing a video and we did not grab a
        # frame, then we have reached the end of the video
        if args.get("video") and not grabbed:
            break
        skin2 = SDF.FrameToSkin(frame2, lower,upper)
        #Returns the highlighted difference between skin frames
        skindiff = SDF.DiffSkin(skin1, skin2)
        cv2.imshow("images", skindiff)
        skin1 = np.copy(skin2)
        	# if the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

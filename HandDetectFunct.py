# -*- coding: utf-8 -*-
import cv2
import numpy as np
import codebook

c = cv2.VideoCapture(0)
c.set(3,320)
c.set(4,240)
cv2.namedWindow('fg',0)
_,img = c.read()
img = cv2.resize(img,(160,120))
h,w = img.shape[:2]
cb = codebook.CodeBook(h,w)
N=0

def mainHandDet():
    while(1):
        global N
        _,img = c.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img,(160,120))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        far = (0,0)
        if N < 10:        
            cb.update(gray)
        else:
            #Getting Background removed image
            fg = cb.foreground(gray)
            #Erroding and then dilating
            element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
            fg = cv2.morphologyEx(fg,cv2.MORPH_OPEN,element)
            #Finding the contours
            contours, hierarchy = cv2.findContours(fg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #Now about to find the largest contour
            #Then Doing Some functions on it
            max_area = 0
            ci = 0
            len_contours = len(contours)
            if len_contours != 0:
                cnt = contours[0]
                for i in range(len(contours)):
                    cnt=contours[i]
                    area = cv2.contourArea(cnt)
                    if(area>max_area):
                        max_area=area
                        ci=i
                    cnt=contours[ci]
                #drawing = np.zeros(img.shape,np.uint8)
                hull = cv2.convexHull(cnt)
                drawing = cv2.cvtColor(np.copy(gray), cv2.COLOR_GRAY2BGR)
                #Drawing contours and hull (contour follows hand, hull is outside)
                cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
                cv2.drawContours(drawing,[hull],0,(0,0,255),2)
                
                
                moments = cv2.moments(cnt)
                if moments['m00']!=0:
                    i=0
                    hull = cv2.convexHull(cnt, returnPoints = False)
                    if(hull.shape[0] > 3):
                        defects = cv2.convexityDefects(cnt,hull)
                        y_points = []
                        if not defects is None:
                            for i in range(defects.shape[0]):
                                s,e,f,d = defects[i,0]
                                far = tuple(cnt[f][0])
                                y_points.append([far[1], i])
                            y_points.sort()
                            indx = y_points[0][1]
                            s, e, f , d = defects[indx, 0]
                            far = tuple(cnt[f][0])
                            cv2.circle(drawing,far,5,[255,0,0],-1)
                        
                cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                hull = cv2.convexHull(cnt,returnPoints = False)
                
                drawing = cv2.resize(drawing, (540,360))
                cv2.imshow('drawing', drawing)
            cv2.imshow('fg',fg)
        N += 1
        if cv2.waitKey(5)==27:
            cv2.destroyAllWindows()
            c.release()
            break
        else:
            yield far

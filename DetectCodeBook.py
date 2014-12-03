# -*- coding: utf-8 -*-
import cv2
import sys
import numpy as np
import time
import cProfile
import pyximport; pyximport.install(reload_support=True,                                     
                                    setup_args={'script_args':["--compiler=mingw32"]})
import codebook
c = cv2.VideoCapture(0)
c.set(3,320)
c.set(4,240)
cv2.namedWindow('vid',0)
cv2.namedWindow('fg',0)
_,img = c.read()
img = cv2.resize(img,(160,120))
h,w = img.shape[:2]
cb = codebook.CodeBook(h,w)
N=0

def fillholes(gray):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    res = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)    

def run():
    while(1):
        global N
        _,img = c.read()
        img = cv2.resize(img,(160,120))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('vid',gray)    
        if N < 10:        
            cb.update(gray)
        else:
            #Getting Background removed image
            fg = cb.fg(gray)
            #Erroding and then dilating
            element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
            fg= cv2.erode(fg,element)
            fillholes(fg)
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
                        print ci
                    cnt=contours[ci]
                #drawing = np.zeros(img.shape,np.uint8)
                hull = cv2.convexHull(cnt)
                drawing = cv2.cvtColor(np.copy(gray), cv2.COLOR_GRAY2BGR)
                #Drawing contours and hull (contour follows hand, hull is outside)
                cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
                cv2.drawContours(drawing,[hull],0,(0,0,255),2)
                #Now finding the center of this hull
                moments = cv2.moments(cnt)
                if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00              
                    centr=(cx,cy)
                    cv2.circle(drawing,centr,5,[0,0,255],2)
                    i=0
                    print len(hull)
                    print len(hull[0])
                    if(len(hull[i]) > 2 ):
                        defects = cv2.convexityDefects(cnt,hull)
                        mind=0
                        maxd=0
                        for i in range(defects.shape[0]):
                            s,e,f,d = defects[i,0]
                            start = tuple(cnt[s][0])
                            end = tuple(cnt[e][0])
                            far = tuple(cnt[f][0])
                            dist = cv2.pointPolygonTest(cnt,centr,True)
                            cv2.line(img,start,end,[255,255,255],2)
                            
                            cv2.circle(img,far,5,[255,255,255],-1)
                        print(i)
                        """
                        if defects.shape[0] >= 3:
                            palm_points = []
                            rough_palm_center = np.array([0,0])
                            for j in xrange(defects.shape[0]):
                                startidx = defects[j][0]
                                endidx=defects[j][1]
                                faridx=defects[j][2]
                                pntStart = (contours[0][startidx])
                                pntEnd = (contours[0][endidx])
                                pntFar = (contours[0][faridx])
                                rough_palm_center += pntStart + pntEnd + pntFar
                                palm_points.append(pntFar)
                                palm_points.append(pntStart)
                                palm_points.append(pntEnd)
                            rough_palm_center[0] /= (defects.shape[0] * 3)
                            rough_palm_center[1] /= (defects.shape[0] * 3)
                            clst_pnt = palm_points[0]
                            distvec = []
                            
                            for k in xrange(len(palm_points)):
                                distvec.append((np.linalg.norm(rough_palm_center, np.array(palm_points[k])),k))
                            distvec.sort()
                            
                            soln_circle = []
                            for m in xrange(defects.shape[0]):
                                if (m + 2 < defects.shape[0]):
                                    p1 = palm_points[defects[i][1]]
                                    p2 = palm_points[defects[i][1]]
                                    p3 = palm_points[defects[i][1]]
                                    """
                cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                hull = cv2.convexHull(cnt,returnPoints = False)
                
                cv2.imshow('drawing', drawing)
            cv2.imshow('fg',fg)
        N += 1
        if cv2.waitKey(5)==27:
            break
run()
cv2.destroyAllWindows()
c.release()

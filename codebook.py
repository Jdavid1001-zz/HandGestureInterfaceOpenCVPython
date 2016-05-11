# -*- coding: utf-8 -*-
#http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.148.9778&rep=rep1&type=pdf

import numpy as np

alpha = 5
beta = 0.95

Tdel = 80
Tadd = 140
Th= 80

mn,mx,f,l,p,q=0,1,2,3,4,5

class CodeBook():
    def __init__(self,height,width):
        self.height = height
        self.width = width
        self.M = np.empty((height, width), dtype=np.object)
        self.H = np.empty((height, width), dtype=np.object)
        filler = np.frompyfunc(lambda x: list(), 1, 1)
        filler(self.M,self.M)
        filler(self.H,self.H)
        self.t = 1

    def updatev(self,gray,cb):
        I,t = gray,self.t     
        if not cb:
            c = [max(0.0,I-alpha),min(255.0,I+alpha),1,t-1,t,t]
            cb.append(c)
        else:
            found = False
            for cm in cb:
                if(cm[mn]<=I<=cm[mx] and not found): 
                    cm[mn] = ((I-alpha)+(cm[f]*cm[mn]))/(cm[f]+1.0)    
                    cm[mx] = ((I+alpha)+(cm[f]*cm[mx]))/(cm[f]+1.0)
                    cm[f] += 1
                    #cm[l] = max(cm[l],t-cm[q])
                    cm[l] = 0
                    cm[q] = t
                    found = True
                else:
                    cm[l] = max(cm[l],10-cm[q]+cm[p]-1)
            if not found:
                c = [max(0.0,I-alpha),min(255.0,I+alpha),1,t-1,t,t]
                cb.append(c)                
        return cb
    def update(self,gray):       
        M = self.M
        updatev = np.vectorize(self.updatev,otypes=[np.object])
        self.M=updatev(gray,M)
        self.t += 1   
    def fgv(self,gray,cwm,cwh):
        I,t = gray,self.t
        found = False
        for cm in cwm:
            if(cm[mn]<=I<=cm[mx] and not found):
                cm[mn] = (1-beta)*(I-alpha) + (beta*cm[mn])
                cm[mx] = (1-beta)*(I+alpha) + (beta*cm[mx])
                cm[f] += 1
                #cm[l] = max(cm[l],t-cm[q])
                cm[l] = 0
                cm[q] = t
                found = True
            else:
                cm[l] += 1
                #cm[l]=max(cm[l],t-cm[q]+cm[p]-1)
        cwm[:] = [cw for cw in cwm if cw[l]<Tdel]  
        if found: return 0
        for cm in cwh:
            if(cm[mn]<=I<=cm[mx] and not found):
                cm[mn] = (1-beta)*(I-alpha) + (beta*cm[mn])
                cm[mx] = (1-beta)*(I+alpha) + (beta*cm[mx])
                cm[f] += 1
                #cm[l] = max(cm[l],t-cm[q])
                cm[l] = 0
                cm[q] = t
                found = True
            else:
                #cm[l]=max(cm[l],t-cm[q]+cm[p]-1)
                cm[l] += 1
        if not found:
            c = [max(0.0,I-alpha),min(255.0,I+alpha),1,0,t,t]
            cwh.append(c)
        cwh[:] = [cw for cw in cwh if cw[l]<Th]
        tomove = [cw for cw in cwh if cw[f]>Tadd]
        cwh[:] = [cw for cw in cwh if not cw in tomove]
        cwm.extend(tomove)
        return 255
    def fg(self,gray):  
        M,H = self.M,self.H
        fgv = np.vectorize(self.fgv,otypes=[np.uint8])
        fg = fgv(gray,M,H)
        self.t += 1
        return fg

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 09:55:13 2018
regionsearch exsample 
find ROI "plate recognize"
@author: zhouwei
"""
import cv2 as cv
import numpy as np
import math 
import os
import shutil
#create output file
filedir = "OUT"
if os.path.exists(filedir):
    shutil.rmtree(filedir)
os.mkdir(filedir)
filepath = "Rawpic/a.jpg"
img00 = cv.imread(filepath)
imgraw = img00.copy()
cv.imwrite(filedir+"/imgraw.jpg",imgraw)

#filter
kernel_size =(5,5)
sigma = 0.0
img01 = cv.GaussianBlur(imgraw,kernel_size,sigma)
cv.imwrite(filedir+"/imgfilter.jpg",img01)
#grady 
img02 = cv.cvtColor(img01,cv.COLOR_RGB2GRAY)

#sobel grade algrithem
imgx = cv.Sobel(img02,-1,1,0)# x grade
imgy = cv.Sobel(img02,-1,0,1)# y grade

absx = cv.convertScaleAbs(imgx)
absy = cv.convertScaleAbs(imgy)

cv.imwrite(filedir+"/absx.jpg",absx)
cv.imwrite(filedir+"/absy.jpg",absy)

imgsobel = cv.addWeighted(absx,1.0,absy,0.0,0)# x weight 1.0 ,y weight 0.0 
cv.imwrite(filedir+"/imgsobel.jpg",imgsobel)

#convert to 2 value 
ret,img03 = cv.threshold(imgsobel,0,255,cv.THRESH_OTSU + cv.THRESH_BINARY)
#
cv.imwrite(filedir+"/imgBinary.jpg",img03)
#close opration
kernel = np.uint8(np.ones((4,10)))
img04 = cv.morphologyEx(img03,cv.MORPH_CLOSE,kernel)
cv.imwrite(filedir+"/imgclose.jpg",img04)
#find external contours
img,coutours,hierarchy = cv.findContours(img04,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
#draw contours 
cv.drawContours(imgraw,coutours,-1,(0,255,0),2)

#HSV COLOR  get region 
'''
imhsv = cv.cvtColor(imgraw,cv.COLOR_BAYER_BG2BGR)
lower = np.array([60,80,80])
upper = np.array([150,255,255])
mask = cv.inRange(imhsv,lower,upper)
mask = cv.morphologyEx(mask,cv.MORPH_CLOSE,kernel)# mask region 
'''

imglist =[]
j =0
for i in coutours:
    imgtmp = imgraw.copy()
    rects = cv.minAreaRect(i)# minize out rect 
    #rects[0] position of top point
    #rects[1][0] 
    #rects[1][1] 
    #rects[2] rotation angle 
    bos = cv.boxPoints(rects)# get 4 point position in (x,y) of rect 
    box = np.int0(bos)
    angle = rects[2]
    width = rects[1][0]
    high = rects[1][1]
    size = rects[1][0]*rects[1][1]
    if width > 20 and high >= 10 and angle > -80:
        if(width/np.float32(high) >= 3.0 or width/np.float32(high) < 0.5):
            cv.drawContours(imgraw,[box],-1,(0,0,255),2)
            
            h0 = img00.shape[0]
            w0 = img00.shape[1]
            degree = angle
            if(width < high):
                degree += 90 
                tmp = h0
                h0 = w0
                w0 = tmp
            centor = (h0/2,w0/2)
            RotateMatrix = cv.getRotationMatrix2D(centor,angle = degree,scale =1)
            #update picture size 
            
            hinew = np.int0(w0*math.fabs(math.sin(math.radians(degree)))+h0*math.fabs(math.cos(math.radians(degree))))
            winew = np.int0(h0*math.fabs(math.sin(math.radians(degree)))+w0*math.fabs(math.cos(math.radians(degree))))
            #update rotation mat
            RotateMatrix[0,2] += (winew - w0)/2
            RotateMatrix[1,2] += (hinew - h0)/2
            # rotate picture 
            imgresult =imgtmp.copy()
            imgresult = cv.warpAffine(imgtmp,RotateMatrix,(hinew,winew))
            
            strname = filedir+"/imgrotate"+np.str(j)+".jpg"
            cv.imwrite(strname,imgresult)
            # region rect pos after rotation
            p1 = list(box[0])
            p2 = list(box[1])
            p3 = list(box[2])
            p4 = list(box[3])
            [[p1[0]],[p1[1]]] = np.int0(np.dot(RotateMatrix,np.array([[p1[0]],[p1[1]],[1]])))
            [[p3[0]],[p3[1]]] = np.int0(np.dot(RotateMatrix,np.array([[p3[0]],[p3[1]],[1]])))
            [[p2[0]],[p2[1]]] = np.int0(np.dot(RotateMatrix,np.array([[p2[0]],[p2[1]],[1]])))
            [[p4[0]],[p4[1]]] = np.int0(np.dot(RotateMatrix,np.array([[p4[0]],[p4[1]],[1]])))
            
            # draw rect after rotation ,this rect is a horizontal 
            cv.line(imgresult,tuple((p1)),tuple((p2)),(0,255,0),2)
            cv.line(imgresult,tuple((p2)),tuple((p3)),(0,255,0),2)
            cv.line(imgresult,tuple((p3)),tuple((p4)),(0,255,0),2)
            cv.line(imgresult,tuple((p4)),tuple((p1)),(0,255,0),2)
            #
            imgROI = imgresult[p2[1]:p4[1],p1[0]:p3[0]]
            imglist.append(imgROI)
            #print(imgROI)
            strname = filedir+"/imgresul"+np.str(j)+".jpg"
            cv.imwrite(strname,imgROI)
            j += 1
            
            
cv.imwrite(filedir+"/Contours.jpg",imgraw)







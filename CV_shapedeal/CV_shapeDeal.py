#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 22:45:33 2018
形态学处理 morphological processing
@author: zhouwei
"""
import cv2 
import numpy as np

img01 = cv2.imread("test01.jpg",0)
'''
opencv can't show picture only use write
cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
cv2.imshow("img01.jpg",img01)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
cv2.imwrite("img01.jpg",img01)
#
#kernel = np.array([[1,0,1],[1,1,1],[0,0,1]])
# kernel correct define as below 
#kernel = np.ones((3,3), np.uint8)#kernel must define type
kernel = np.uint8(np.ones((3,3)))

print(kernel)
'''
#pengzhang 
dilatepic = cv2.dilate(img01,kernel)
cv2.imwrite("dilatepic.jpg",dilatepic)
'''
''''
#fushi
erodepic = cv2.erode(img01,kernel)
cv2.imwrite("erodepic.jpg",erodepic)
'''

m = img01.shape[0]
n = img01.shape[1]
print(img01.shape)

#revert gray 
#cv2 has it's owne func :bitwise_not 
'''
for i in range(m):
    for j in range(n):
        img01[i][j] = 255 - img01[i][j]


cv2.imwrite("imgrevert.jpg",img01)
'''
'''
#add noise 

for i in range(8000):
    x=np.random.randint(0,m)
    y=np.random.randint(0,n)
    img01[x][y]=255 ###255 means bright best
'''

cv2.imwrite("imgaddnoise.jpg",img01)
# fushi & pengzhang all for white color (gred ==255)

#fushi decress noise 
erodepic = cv2.erode(img01,kernel)
cv2.imwrite("erodepic.jpg",img01)

#pengzhang incress noise 
dilatepic = cv2.dilate(img01,kernel)
cv2.imwrite("dilatepic.jpg",dilatepic)


#close  pengzhang + fushi  incress white noise
closepic = cv2.morphologyEx(img01,cv2.MORPH_CLOSE,kernel)


#open= fushi+pengzhang  decress white noise 

openpic = cv2.morphologyEx(img01,cv2.MORPH_OPEN,kernel)

cv2.imwrite("closepic.jpg",closepic)
cv2.imwrite("openpic.jpg",openpic)


#find edge
#将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
edge = cv2.absdiff(dilatepic,erodepic)

cv2.imwrite("edge.jpg",edge)
#binary pic
#上面得到的结果是灰度图，将其二值化以便更清楚的观察结果
retval, edge = cv2.threshold(edge, 40, 255, cv2.THRESH_BINARY)

cv2.imwrite("edge01.jpg",edge)

#反色，即对二值图每个像素取反
edge02 = cv2.bitwise_not(edge)

cv2.imwrite("edge02.jpg",edge02)



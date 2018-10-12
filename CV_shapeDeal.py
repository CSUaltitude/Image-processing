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

#revert gred 
'''
for i in range(m):
    for j in range(n):
        img01[i][j] = 255 - img01[i][j]


cv2.imwrite("imgrevert.jpg",img01)
'''
#add noise 
for i in range(8000):
    x=np.random.randint(0,m)
    y=np.random.randint(0,n)
    img01[x][y]=255 ###255 means bright best
    
cv2.imwrite("imgaddnoise.jpg",img01)

#fushi
erodepic = cv2.erode(img01,kernel)
cv2.imwrite("erodepic.jpg",erodepic)
#pengzhang 
dilatepic = cv2.dilate(erodepic,kernel)
cv2.imwrite("dilatepic.jpg",dilatepic)

#close 
closepic = cv2.morphologyEx(img01,cv2.MORPH_CLOSE,kernel)


#open
openpic = cv2.morphologyEx(img01,cv2.MORPH_OPEN,kernel)

cv2.imwrite("closepic.jpg",closepic)
cv2.imwrite("openpic.jpg",openpic)






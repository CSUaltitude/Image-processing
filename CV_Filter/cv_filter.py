#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 21:37:29 2018
#Image  filter 
@author: zhouwei
"""
import cv2
import numpy as np


img00 = cv2.imread("test01.jpg",0)

#add noise 
for i in range(5000):
    x = np.random.randint(0,img00.shape[0])
    y = np.random.randint(0,img00.shape[1])
    img00[x][y] = 255

cv2.imwrite("img00.jpg",img00)

#gassian filter
'''
filter mat like :
0.8  0.9  0.8
0.9  1.0  0.9
0.8  0.9  0.8
'''



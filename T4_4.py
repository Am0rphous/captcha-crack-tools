#-*- coding: utf-8 -*-
#
import cv2
import numpy as np



#img = np.zeros((4,4), np.uint8)

"""
img[1, 0]=1
img[2, 0]=1
img[0, 3]=1
img[0, 2]=1
img[1, 2]=1
###
img[0, 0]=1
img[0, 2]=1
img[0, 1]=1
#img[0, 3]=1
#img[1, 0]=1
#img[3, 0]=1
#img[2, 2]=1
img[1, 3]=1
img[2, 3]=1
#img[3, 2]=1
img[3, 3]=1
###
img[0, 0]=1
img[0, 2]=1
#img[0, 1]=1
#img[0, 3]=1
img[1, 0]=1
#img[3, 0]=1
#img[2, 2]=1
#img[1, 3]=1
img[2, 3]=1
img[3, 2]=1
img[3, 3]=1
"""

def func_o(img):
        nonzero = np.argwhere(img>0)
        g = 0
        dk = {}
        def r_func(x,y):
                    for i in y:
                        if i in x:
                               y.remove(i)
                               x += y
                               r_func(list(set(x)),y)

        for idx, val in enumerate(nonzero):
                #print idx, val
                dk[idx] = [] 
                for index, value in enumerate(np.ndenumerate(img)):
                    if value[1] == 1:
                        #print index, value[0], idx, val, np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2)
                        if np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2) == 0:
                            #print 'NULL', val, value[0], idx, index
                            dk[idx].append(index)
                        if np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2) == 1:
                            #print 'ONE', val, value[0], idx 
                            dk[idx].append(index)
                        if np.sqrt((val[0] - value[0][0]) ** 2 + (val[1] - value[0][1]) ** 2) == 1.4142135623730951:
                            #print 'ONE_1', val, value[0], idx
                            dk[idx].append(index)

        #print "DDDKk",dk

        ng = {}
        for i in dk.keys():
            for ii in dk.keys():
               if ii != i: 
                  
                  g = r_func(dk[i], dk[ii])
                  #print i, g
                  #if g is not None:
                  #   ng[i] = g

        return dk


# -*- coding:utf-8 -*-


import tensorflow as tf
import cv2
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

#img = cv2.resize(cv2.imread("/media/sadko/1b32d2c7-3fcf-4c94-ad20-4fb130a7a7d4/PLAYGROUND/RL/data/taxi4x4/img/41409.jpg"), (416, 416))

def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def draw_boxes(image):

        h_z = 416 / 4
        image[0:, h_z:(h_z+5), :] = 255
        image[0:, (h_z*2):((h_z*2)+5), :] = 255
        image[0:, (h_z*3):((h_z*3)+5), :] = 255
        image[0:, (h_z*4):((h_z*4)+5), :] = 255
        # w line
        #      x          y
        image[h_z:(h_z+5), 0:, :] = 255
        image[(h_z*2):((h_z*2)+5), 0:, :] = 255
        image[(h_z*3):((h_z*3)+5), 0:, :] = 255
        image[(h_z*4):((h_z*4)+5), 0:, :] = 255

        return image
#img = draw_boxes(img)
#imgs(img)
def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 'q':
        print(object_list)
        tl_list = []
        br_list = []
        object_list = []
        img = None

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata

    print 'x = %d, y = %d'%(ix, iy), event.inaxes.get_gid() #inaxes
    arrr_idx.append(event.inaxes.get_gid())
    #global coords
    #coords = [ix, iy]

    #return coords

def quit_figure(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)


def window_slide(image):
        stepSize = 104
        (w_width, w_height) = (104, 104) # window size
        arrr = []
        fig, ax = plt.subplots(4, 4)
        idxAX = 0
        for ii, x in enumerate(range(0, image.shape[1], stepSize)):
           for iii,y in enumerate(range(0, image.shape[0], stepSize)):
        #for x in range(0, 4):
        #    for y in range(0, 4): 
              idxAX += 1
              print x,y, idxAX# x + w_width, y, y + w_height, image.shape[1] - w_width, stepSize
              window = image[x:x + w_width, y:y + w_height, :]
              arrr.append(window)
              ax[ii, iii].imshow(window)
              ax[ii, iii].set_gid(idxAX)
        #print len(arrr)


        #fig.connect('button_press_event', onclick)
        global arrr_idx
        arrr_idx = []
        #plt.connect('button_press_event', onclick)
        plt.connect('button_press_event', onclick)


        cid = plt.gcf().canvas.mpl_connect('key_press_event', quit_figure)
        plt.show()
        
        return arrr, arrr_idx



#iop = window_slide(img)
#print iop[1]

def getV(x,y):
    #print x, y
    for i in y:
        x[i-1] = 1.
    return x

#ans_V = np.zeros([16])
#ans_V = getV(ans_V, iop[1])

#print ans_V



lists = ["data/taxi4x4/big_img.csv", "data/bicycles4x4/big_img.csv"]

humanANSW = {}

for jk in lists:
                clas = jk.split("/")[1]
                #print clas
                files = open(jk, 'r').readlines()
                for igh, gh in enumerate(files[:]):
                          gh = gh.split('\n') 
                          gh = gh[0].split(';')
                          namefile = 'data/'+clas+'/img/'+gh[0]+'.jpg'
                          if gh[1] != 'no_matching_images':
                                  img = cv2.resize(cv2.imread(namefile), (416, 416))
                 
                                  convRUC = [int(i) for i in gh[1].split(':')[1].split('/')]
                                  ans_V = np.zeros([16]) # answer in vector
                                  ans_V = getV(ans_V, convRUC)
                                  
                                  iop = window_slide(img)

                                  ans_A = np.zeros([16])
                                  ans_A = getV(ans_A, iop[1])
                                  print ans_A, ans_V, namefile
                                  humanANSW[namefile] = [ans_A, ans_V]



print humanANSW





"""
#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
events = [i for i in dir(cv2) if 'EVENT' in i]
#print events

def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print x,y
        #cv2.circle(img,(x,y),100,(255,0,0),-1)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()


a_t = np.zeros([4])

a_t[random.randrange(0, 2)] = 1
a_t[random.randrange(2, 4)] = 1

a_t_a = a_t[:2]
a_t_c = a_t[2:]

at0 = np.concatenate((a_t_a,a_t_c), axis=None)#np.vstack(()) 

action_index = np.argmax(a_t_c)

print a_t, a_t_c, a_t_a, at0, action_index
"""



#-*- coding: utf-8 -*-
#
import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt



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

    global coords
    coords = [ix, iy]

    return coords


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
        plt.connect('button_press_event', onclick)
        plt.show()
        return arrr


with open('data/bicycles4x4/big_img.csv', 'r') as g:
     for gh in g:
         gh = gh.split('\n') 
         gh = gh[0].split(';')
         namefile = gh[0]
         try:
                 gh = gh[1].split(':')[1]
                 namefile = 'data/bicycles4x4/img/'+namefile+'.jpg'

                 iop = cv2.imread(namefile)
                 iop = cv2.resize(iop, (416, 416))
                 
                 
                 """
                 iop[0:, 104:(104+5), :] = 255
                 iop[0:, 208:(208+5), :] = 255
                 iop[0:, 312:(312+5), :] = 255
                 iop[0:, 416:(416+5), :] = 255
                 # w line
                 #      x          y
                 iop[104:(104+5), 0:, :] = 255
                 iop[208:(208+5), 0:, :] = 255
                 iop[312:(312+5), 0:, :] = 255
                 iop[416:(416+5), 0:, :] = 255
                 #print gh.split('/')
                 """
                 iop = window_slide(iop)#getline(iop)
                 
                 #print iop[0].shape
                 #for ixxx in range(len(iop)):
                     #pass
                     #imgs(iop[ixxx])
                 #    ax[0, 0].imshow(iop[ixxx])
                     #plt.imshow(iop[ixxx])
                 #    plt.show()

         except IndexError:
                 print gh

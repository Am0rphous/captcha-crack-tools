#-*- coding: utf-8 -*-
#
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from matplotlib.widgets import RectangleSelector
#from generate_xml import write_xml
import glob, random
import json

# VISUAL
def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

def from_yolo_to_cor(box, shape):
    img_h, img_w, _ = shape
    # x1, y1 = ((x + witdth)/2)*img_width, ((y + height)/2)*img_height
    # x2, y2 = ((x - witdth)/2)*img_width, ((y - height)/2)*img_height
    #------------
    x1, y1 = int((box[0] + box[2]/2)*img_w), int((box[1] + box[3]/2)*img_h)
    x2, y2 = int((box[0] - box[2]/2)*img_w), int((box[1] - box[3]/2)*img_h)
    #WORK
    #x1, y1 = int((box[0] + box[2]/2)*416), int((box[1] + box[3]/2)*416)
    #x2, y2 = int((box[0] - box[2]/2)*416), int((box[1] - box[3]/2)*416)
    return x1, y1, x2, y2
    
def draw_boxes(img, boxes):
    #for box in boxes:
    x1, y1, x2, y2 = from_yolo_to_cor(boxes, img.shape)
    #print x1, y1, x2, y2
    img = cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 3)
    
    return img
# END VISUAL ------------------------------------->

F = open('TR0.txt','r')
F = F.readlines()
for ix, i in enumerate(F[:]):
    name = i.split('\n')[0].split('/')[-1].split('.')[0]
    name = "/home/sadko/labels/motos4x4/" + name + ".txt"
    #print i 
    iop = cv2.imread('motos4x4/'+i.split('\n')[0].split('/')[-1])
    G = open(name,'r')
    G = G.readlines()

    img_resized = cv2.resize(iop, (416, 416))
    #img_resized = np.reshape(img_resized, [416, 416, 3])
    print ix, img_resized.shape
    for ii in (G):
        box = ii.split('\n')[0].split(' ')[1:]
        box = [float(x) for x in box]
        #print box
        draw_boxes(img_resized, box)
    imgs(img_resized)

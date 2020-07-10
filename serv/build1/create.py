# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os, sys, io
import glob, base64, json, time


o_dict = {}


def imgs(x):
      cv2.imshow('Rotat', x)#np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()



def parseIMG(dir_name):
                files = []
		path = dir_name
                print "PARSING",path
		valid_images = [".jpg", ".png", ".JPG", ".JPEG", ".PNG", ".jpeg"]
                #valid_images = [".MOV", ".mp4", ".MP4"]
		for r, d, f in os.walk(path):
		    #print r, d, f
		    for file in f:
                      for in_g in valid_images:
			if in_g in file:
                           print file.split("_")[0]
                           #file_path = os.path.join(r, file)
                           #o_dict[file.split("_")[0]] = [os.path.join(r, file)]
                           #files.append([os.path.join(r, file)])
                           try:
                             o_dict[file.split("_")[0]].append(os.path.join(r, file))
                           except KeyError:
                             o_dict[file.split("_")[0]] = [os.path.join(r, file)]
                           #if os.path.isfile(file_path):
                              #os.remove(file_path)
                return files      

def cutimg(data, col):
                ans = []
	        im_w, im_h, im_c = 300, 300, 3
                imzero = np.zeros(shape=(im_w, im_h, im_c), dtype=np.uint8)
                w, h = im_w//col, im_h//col
		w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
		for wi in range(0, w_num):
		    for hi in range(0, h_num):
                        imzero[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :] = data[num]
                        num += 1


                return imzero





f1 = parseIMG("bridges")
f2 = parseIMG("not_bridges")

print o_dict  #f1, len(f1), len(f2)

for u in o_dict.keys():
   #print o_dict[u]#.sort()
   s_dict = {}
   for p in o_dict[u]:
       #print p, p.split(".")[0].split("_")[-1]
       s_dict[p.split(".")[0].split("_")[-1]] = p
   l_data = []
   for k in sorted(s_dict.keys()):
       #print s_dict[k]
       iop = cv2.imread(s_dict[k])
       #imgs(iop)
       #print iop.shape, iop[:2,:2,:]
       l_data.append(iop)
   
   iop = cutimg(np.array(l_data),3)   

   print iop.shape
   imgs(iop)
   


"""
def cop(x, y):
     f_file = open(x, "rb").read()
     to_file = open(y,"wb").write(f_file)

for ix, h in enumerate(files):
    print ix, h[0], h[0].split("/")[-1]

    #cop(h[0], "FOTO/"+h[0].split("/")[-1])

"""

"""

    im = cv2.imread(h[0])
    try:
      cv2.imshow('frame',im)
    except:
      os.remove(h[0])
files2 = []

for ih, h in enumerate(files):
  for ig, g in enumerate(files):
     if h[0].split("/")[-1] == g[0].split("/")[-1]:
          if h[0] != g[0]:
                 
                 fl1 = open(h[0], "rb").read()
                 fl2 = open(g[0], "rb").read()
                 if fl1 == fl2:
                     print h[0],g[0]
                 #files2.append([h[0],g[0]])
#print len(files2)
    #print ix, h[0], h[0].split("/")[-1]
    #cop(h[0], "FOTO_2/"+h[0].split("/")[-1])
"""

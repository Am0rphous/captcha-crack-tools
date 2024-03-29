# -*- coding: utf-8 -*-
import cv2, os, glob, time, requests, json
import numpy as np

import base64, glob
from tornado.escape import json_encode

size = 416


def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()



def draw_lines(image, col):
     h_z = size / col
     image[0:, h_z:(h_z+5), :] = 255
     image[0:, (h_z*2):((h_z*2)+5), :] = 255
     image[0:, (h_z*3):((h_z*3)+5), :] = 255
     image[0:, (h_z*4):((h_z*4)+5), :] = 255
     #      x          y
     image[h_z:(h_z+5), 0:, :] = 255
     image[(h_z*2):((h_z*2)+5), 0:, :] = 255
     image[(h_z*3):((h_z*3)+5), 0:, :] = 255
     image[(h_z*4):((h_z*4)+5), 0:, :] = 255
     



class record():
     def __init__(self):
         self.file = open('hydrantsMore.zip.txt', 'w')
     def save(self, i):
         #print i
         self.file.write(i+"\n") 

"""
def LeoPost(x, idx, task):
    url = "http://148.251.0.181:8084/"
    with open(x, "rb") as f:
            data = f.read()
            data = base64.b64encode(data).decode("utf-8")
            payload = {"image":data, "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task}
            headers = { 'Content-Type': "application/json",
                        'cache-control': "no-cache" }
            response = requests.request("POST", url, data=json_encode(payload), headers=headers)
            
            print (json.loads(response.text))
"""

def LeoPost(data, idx, task):
    url = "http://148.251.0.181:8084/"
    _, data = cv2.imencode('.jpg', data) #base64.b64encode(data.encode())#str(data.encode("base64"))
    data = base64.b64encode(data).decode("utf-8")
    #print data, type(data)
    payload = {"image":data, "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task}
    headers = { 'Content-Type': "application/json",
                'cache-control': "no-cache" }
    response = requests.request("POST", url, data=json_encode(payload), headers=headers)
    return json.loads(response.text)


def deansw(x):
    s = []
    for ix, i in enumerate(x):
        #print ix, i
        if int(i) == 1:
           s.append(ix+1)
    return s

def cutimg(data, idx, task ,col):
	if True:
                ans = []
                #print (data.shape)
                im_w, im_h, im_c = data.shape
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
                for wi in range(0, w_num):
                   for hi in range(0, h_num):
                        num += 1
                        #imgs(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                        #cutpart = str(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :]).encode("base64")
                        an = LeoPost(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :], idx, task)
                        #print an
                        ans.append(an['text'][0])
                        #imgs(i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                #print deansw(ans)
                return deansw(ans)


def parseIMG(dir_name):
    files = {}
    csv = ""
    path = dir_name
    print ("PARSING",path)
    valid_images = [".jpg",".png"]
    for r, d, f in os.walk(path):
	#print r, d, f
        for file in f:
           if valid_images[0] in file or valid_images[1] in file:
               files[file.split(".")[0]] = [os.path.join(r, file)]
           if ".csv" in file:
               csv = os.path.join(r, file)
    return files, csv

if __name__ == "__main__":
   #print "START"
   FL = parseIMG("data/hydrantsWarningStep.zip")
   #print (FL[0])
   for ix, u in enumerate(list(FL[0].keys())):
       #print (FL[0][u])
       iop = cv2.imread(FL[0][u][0])
   
       #imgs(iop)
       PP = cutimg(iop, ix, 'hydrants3', 3)
       
       P = LeoPost(iop, ix, 'hydrants')
       print ("Start Post", PP, P)
       #print(PP)


   """
4x4:
mountains
palms
hydrants	
buses
crosswalks
traffic_lights
chimneys
stairs
motorbike
bicycles
tractors
taxi
bridges


3x3/2x4:
cars
stores
bridges
vehicles
buses3
traffic_lights3
crosswalks3
boats3
bicycles3
taxi3
sculptures3
motos3
hydrants3
tractors3
chimneys3
stairs3
trees3

   """

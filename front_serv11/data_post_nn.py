# -*- coding: utf-8 -*-
import numpy as np
import threading, cv2, os, time, requests, json, base64
from tornado.escape import json_encode
import data_base
from bson.objectid import ObjectId


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
     def __init__(self,idx):
         self.file = open(str(idx)+'_error.txt', 'w')
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
                try: 
                        #print "post>"
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
                except IndexError: 
                   pass

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

def thread_function(new,idx, data, data_d, task):
   #R = record(idx)
   for ix, u in enumerate(data):
          iop = cv2.imread(u["file"])
          
          #PP = cutimg(iop, ix, 'hydrants3', 3)
          PP = LeoPost(iop, ix, task)#(iop, ix, 'hydrants3')
          
          posttoCH = new.see_post(ObjectId(u["_id"]))
          print ("Leopost", posttoCH, [int(x) for x in PP["text"]])
          posttoCH["answ_L"] = [int(x) for x in PP["text"]]
          new.upd_post(ObjectId(u["_id"]), posttoCH)

          #R.save(u+";"+str(PP))
          
          

if __name__ == "__main__":
   new = data_base.mDB()
   new.create_collection("traffic_lights4x4.tar.gz_2019-12-21 16:07:16")#("hydrants error.zip_2019-12-21 16:03:34")
   L = new.see_all_post()
   print ("START")

"""
   im_w = len(L)
   w = im_w//20
   w_num = int(im_w/w)
   num = 0 
   for ix in range(0, w_num):
       f_list = L[ix*w:(ix+1)*w]
       #thread_function(ix, f_list, L)
       x = threading.Thread(target=thread_function, args=(ix, f_list, L))
       x.start()
       #print (f_list[:3],len(f_list))
   #R = record()
   
   FL = parseIMG("holo/DynamicMoreHydrants")
   #print (FL[0])
   im_w = len(list(FL[0].keys()))
   w = im_w//20
   w_num = int(im_w/w)
   num = 0
   for ix in range(0, w_num):
           #print len(list(FL[0].keys())[id*w:(id+1)*w])

           #print len(list(FL[0].keys())[ix*w:(ix+1)*w])
           f_list = list(FL[0].keys())[ix*w:(ix+1)*w]
            
           #thread_function(ix, f_list, FL[0])
           x = threading.Thread(target=thread_function, args=(ix, f_list, FL[0]))
           x.start()

   for ix, u in enumerate(list(FL[0].keys())):
       #print (FL[0][u])
       iop = cv2.imread(FL[0][u][0])
   
       #imgs(iop)
       PP = cutimg(iop, ix, 'hydrants3', 3)
       
       #P = LeoPost(iop, ix, 'hydrants')
       print ("Start Post", PP)#, P)
       R.save(FL[0][u][0]+";"+str(PP))
       #print(PP)


   

import threading
import logging
import time

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    threads = list()
    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()
    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

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

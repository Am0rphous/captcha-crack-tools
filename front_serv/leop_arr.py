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
     def __init__(self,idx):
         self.file = open(str(idx)+'_Arr.txt', 'w')
     def save(self, i):
         #print i
         self.file.write(i+"\n") 
"""
class record():
     def __init__(self):
         self.file = open('hydrantsMore.zip.txt', 'w')
     def save(self, i):
         #print i
         self.file.write(i+"\n") 


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
"""


def deansw(x):
    s = []
    for ix, i in enumerate(x):
        #print ix, i
        if int(i) == 1:
           s.append(ix+1)
    return s

def cutimg(data, idx, task ,col):
        url = "http://148.251.0.181:8084/"
        R = record(idx)
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
                        _, _data = cv2.imencode('.jpg', data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                        _data = base64.b64encode(_data).decode("utf-8")
                        #print an
                        ans.append({"image":_data, "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task})
                        #imgs(i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                #print ans
                #ans = json.dumps(ans).encode()
                R.save(str(json_encode(ans)))
                headers = { 'Content-Type': "application/json",
                            'cache-control': "no-cache" }
                response = requests.request("POST", url, data=json_encode(ans), headers=headers)
                print json.loads(response.text)

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

#part

if __name__ == "__main__":
   #print "START"
   #R = record()
   FL = parseIMG("data/warning_stepsHydrants")
   #print (FL[0])
   for ix, u in enumerate(list(FL[0].keys())):
       #print (FL[0][u])
       iop = cv2.imread(FL[0][u][0])
   
       #imgs(iop)
       PP = cutimg(iop, ix, 'hydrants3', 3)
       
       #P = LeoPost(iop, ix, 'hydrants')
       print ("Start Post", PP)#, P)
       #R.save(FL[0][u][0]+";"+str(PP))
       #print(PP)


   """

pics = ['.jpg', 'jpeg', '.gif', '.png']
files = [f for f in sorted(os.listdir(args.dir))[args.range[0]:args.range[1]] if f[-4:] in pics]

images = []

for file in files:
   with open(os.path.join(args.dir, file), 'rb') as f:
      images.append(f.read())

images = [b64encode(i) for i in images]
type_ = {'type': args.type} if args.type else {}

payload = [{"id": f[:-4], "image": i.decode(), "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", **type_} for i, f in zip(images, files)]

if len(payload) == 1:
   payload = payload[0]

try:
   req = Request('http://%s:%d/' % (args.host, args.port))
   req.add_header('Content-Type', 'application/json')

   jsondata = dumps(payload).encode()

   jsonresp = urlopen(req, data=jsondata).read()
   resp = loads(jsonresp)

   if 'error' in resp:
      sys.exit('error on server')

except ConnectionRefusedError as e:
   print(e)


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

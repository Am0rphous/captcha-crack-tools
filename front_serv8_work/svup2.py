# -*- coding: utf-8 -*-
from pymongo import MongoClient
from tornado.escape import json_encode
from bson.objectid import ObjectId
from tornado.escape import json_encode

import cv2
import numpy as np
import os, sys, io
import glob, base64, json, time

from zipfile import ZipFile
import tarfile
import requests

import tornado.ioloop
import tornado.web
import tornado.websocket

import db1
from l_post import *

mgDC = ["mountains",
               "cars",
               "palms",
               "hydrants",	
               "buses",
               "crosswalks",
               "traffic_lights",
               "chimneys",
               "stairs",
               "motorbike",
               "bicycles",
               "tractors",
               "taxi",
               "bridges"]

# База данных

new = db1.mDB()  


class DATA(object):
        def __init__(self):
            self.file = {}
            self.csv = "";
            
        def parseCSV(self):
              with open(self.csv, 'r') as g:
                             for gh in g.readlines():
                                         gh = gh.split('\n')[0].split(';') 
                                         try:
                                              list = self.file[gh[0]]
                                              if gh[1] != 'no_matching_images':
                                                  convRUC = [int(i) for i in gh[1].split(':')[1].split('/')]
                                                  list.append(convRUC)
                                                  self.file[gh[0]] = list
                                              else:
                                                  list.append([])
                                                  self.file[gh[0]] = list
                                         except KeyError:
                                              pass

        def parseIMG(self, dir_name):
                path = "data/"+dir_name
                print ("PARSING",path)
                valid_images = [".jpg",".png"]
                for r, d, f in os.walk(path):
                    for file in f:
                        if valid_images[0] in file or valid_images[1] in file:
                           self.file[file.split(".")[0]] = [os.path.join(r, file)]
                        if ".csv" in file:
                           self.csv = os.path.join(r, file)

def LeoPost(data, idx, task):
    url = "http://148.251.0.181:8084/"
    _, data = cv2.imencode('.jpg', data) #base64.b64encode(data.encode())#str(data.encode("base64"))
    data = base64.b64encode(data).decode('utf-8')
    #print data, type(data)
    payload = {"image":data, "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":"hydrants3"}
    headers = { 'Content-Type': "application/json",
                'cache-control': "no-cache" }
    response = requests.request("POST", url, data=json_encode(payload), headers=headers)
    return json.loads(response.text)


def deansw(x):
    s = []
    for ix, i in enumerate(x):
        if i == 1:
           s.append(ix+1)
    return s


def ViPost(x, idx, task, c_box):
    url = "http://178.158.131.41:9900/"
    with open(x, "rb") as f:
            data = f.read()
            data = base64.b64encode(data).decode('utf-8')
            payload = {"image":data, "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task, "c_box": c_box }
            headers = { 'Content-Type': "application/json",
                        'cache-control': "no-cache" }
            response = requests.request("POST", url, data=json_encode(payload), headers=headers)
            return json.loads(response.text)



def imgbite(x):
           x = cv2.resize(x,(412,412))
           img = x.astype(np.uint8)
           _, img_str = cv2.imencode('.jpg', img)
           BS = img_str.tobytes()
           return BS


def newimg(data, col):
                ans = []
                im_w, im_h, im_c = col*100, col*100, 3
                imzero = np.zeros(shape=(im_w, im_h, im_c), dtype=np.uint8)
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
                #print (data)
                for wi in range(0, w_num):
                   for hi in range(0, h_num):
                        imzero[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :] = data[num]
                        num += 1


                return imzero


def deansw(x):
    s = []
    for ix, i in enumerate(x):
        if i == 1:
           s.append(ix+1)
    return s


def cutimg(name, data, idx, answ, task, col, collectionName):
	if True:
                im_w, im_h, im_c = data.shape
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
                ls = []
                try: 
                        #print "post>"
                        for wi in range(0, w_num):
                           for hi in range(0, h_num):
                                num += 1
                                y = "data/"+ collectionName + "/"+str(num)+str(idx)+"_"+name.split("/")[-1]
                                cv2.imwrite(y, data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                                if num in answ:
                                   post_s = {"file": y, "_type":col, "_task":task,
                                           "answ": "", "answ_H": "",
                                           "answ_L" : "", "answ_V": [1]}
                                   ls.append(post_s)
                                else:
                                   post_s = {"file": y,  "_type":col, "_task":task,
                                             "answ": "", "answ_H": "",
                                             "answ_L" : "", "answ_V": [0]}
                                   ls.append(post_s)

                        return ls
                except IndexError: 
                   pass 
                

class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    myfile = 0
    seeidx = 0
    name = "" 
    tempID = 0 
    temp_data = [] 
    temp_idx_s = 0
    temp_idx_f = 0  
    temp_4idx = 0

    def track_progress(self, x):
       for member in x:
              self.write_message(json.dumps({"Process": "load"}))
       

    def open(self):
        ImageWebSocket.clients.add(self)
        print("WebSocket opened from: " + self.request.remote_ip)


    def on_message(self, message):
        
                ms =  json.loads(message)
                if list(ms.keys())[0] == "Start":
                   """Начало загрузки"""

                   self.name = ms["Start"]["Name"]
                   try:
                           self.myfile = open("archiv/"+ms["Start"]["Name"], "wb")
                           self.write_message(json.dumps({"Process": "MoreData"}))
                   except IOError:
                           os.mkdir("archiv")
                           self.myfile = open("archiv/"+ms["Start"]["Name"], "wb")
                           self.write_message(json.dumps({"Process": "MoreData"}))
                           
                if list(ms.keys())[0] == "Upload":
                   """Процесс загрузки"""

                   da = ms["Upload"]["Data"]
                   da = da.split(",")[1]
                   file_bytes = io.BytesIO(base64.b64decode(da)).read()
                   self.myfile.write(file_bytes)
                   self.write_message(json.dumps({"Process": "MoreData"}))

                if list(ms.keys())[0] == "Done":
                   """Конец загрузки"""

                   self.myfile.close()
                   self.write_message(json.dumps({"Process": "Process"}))
                      
                if list(ms.keys())[0] == "Process":
                           HD = DATA()
                           lss = ["gz", "tar", "xz"]
                           if self.name.split(".")[-1] in lss:
                                   tar = tarfile.open("archiv/"+self.name, "r")
                                   tar.extractall("data/"+self.name, members=self.track_progress(tar))
                                   tar.close()
                                   HD.parseIMG(self.name)
                                   try:
                                     HD.parseCSV()
                                   except:
                                     pass
                           if self.name.split(".")[-1] == "zip":
                                   zip = ZipFile("archiv/"+self.name)
                                   zip.extractall("data/"+self.name)
                                   
                                   HD.parseIMG(self.name)
                                   try:
                                     HD.parseCSV()
                                   except:
                                     pass
                                     
                                     

                           #######################
                          ###   1 x 1 #############
                           ####################### 
                             
                           if int(ms["type"]) == 1:
                                 collectionName = self.name+"_"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                                 try:
                                    os.mkdir("data/"+collectionName)
                                 except:
                                    pass
                                 collectionName = self.name+"_"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                                 obj = {
                                        "type": '1x1',
                                        "task": ms["task"],
                                        "imageType": 'partial',
                                        "collectionName": collectionName,
                                        "path": ""
                                        }
                                 new.create_collection("collection")
                                 new.create_post(obj)
                                 new.create_collection(collectionName)
                                 try:   
                                         for ixx, fx in enumerate(list(HD.file.keys())[:]):
                                                   file_n = HD.file[fx][0]
                                                   try:
                                                      answ_H = HD.file[fx][1]
                                                   except IndexError:
                                                      answ_H = ""
                                                   if file_n.split("/")[-2].split("_")[0]=="not":
                                                      answ_H = ""
                                                   else:
                                                      answ_H = [1]
                                                   
                                                   iop = cv2.imread(file_n)
                                                   answ_V = ViPost(file_n, str(ixx), ms["task"], int(ms["type"]))
                                                   post_s = {"file": file_n,  "_type":ms["type"], "_task":ms["task"],
                                                             "answ": "", "answ_H": answ_H,
                                                             "answ_L" : "", "answ_V": answ_V["text"]}
                                                   ixx = new.create_post(post_s) #

                                 except KeyboardInterrupt:
                                                 print ("open")
                                                 pass
                                 temp_list = new.see_all_post()
                                 
                                 im_w = len(temp_list)
                                 print ("START", temp_list, im_w)
                                 w = im_w//10
                                 print ("START", temp_list, im_w, w)
                                 w_num = int(im_w/w)
                                 num = 0 
                                 for ix in range(0, w_num):
                                               f_list = temp_list[ix*w:(ix+1)*w]
                                               #thread_function(ix, f_list, L)
                                               x = threading.Thread(target=thread_function, args=(new,ix, f_list, temp_list, ms["task"]+"3"))
                                               x.start()
                                 self.write_message(json.dumps({"Process": "loaddone"})) 
#                                 
                                                                
                           #######################
                          ###   3 x 3 #############
                           #######################  
                                     
                           if int(ms["type"]) == 3:
                                 collectionName = self.name+"_"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                                 try:
                                    os.mkdir("data/"+collectionName)
                                 except:
                                    pass
                                 collectionName = self.name+"_"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                                 obj = {
                                        "type": '3x3',
                                        "task": ms["task"],
                                        "imageType": 'partial',
                                        "collectionName": collectionName,
                                        "path": ""
                                        }
                                 new.create_collection("collection")
                                 new.create_post(obj)
                                 new.create_collection(collectionName)
                                 try: 
                                         for ixx, fx in enumerate(list(HD.file.keys())[:]):
                                                   file_n = HD.file[fx][0]
                                                   try:
                                                      answ_H = HD.file[fx][1]
                                                   except IndexError:
                                                      answ_H = ""

                                                   iop = cv2.imread(file_n)
                                                   answ_V = ViPost(file_n, str(ixx), ms["task"], int(ms["type"])) 
                                                   PP = cutimg(file_n, iop, ixx, [int(x) for x in answ_V["text"]], ms["task"], int(ms["type"]), collectionName)
                                                   
                                                   ixx = new.create_many(PP)
                                 except KeyboardInterrupt:
                                                 print ("open")
                                                 pass
                                                 
                                 temp_list = new.see_all_post()
                                 
                                 im_w = len(temp_list)
                                 print ("START", temp_list, im_w)
                                 w = im_w//10
                                 print ("START", temp_list, im_w, w)
                                 w_num = int(im_w/w)
                                 num = 0 
                                 for ix in range(0, w_num):
                                       f_list = temp_list[ix*w:(ix+1)*w]
                                       if ms["task"] != "cars":
                                          T_task = ms["task"]+"3"
                                       else:
                                          T_task = ms["task"]
                                       x = threading.Thread(target=thread_function, args=(new,ix, f_list, temp_list, T_task))
                                       x.start()
                                 
                                 self.write_message(json.dumps({"Process": "loaddone"}))
                               
                           #######################
                          ###   4 x 4 #############
                           #######################   
                           if int(ms["type"]) == 4:
                                 collectionName = self.name+"_"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                                 try:
                                    os.mkdir("data/"+collectionName)
                                 except:
                                    pass
                                 collectionName = self.name+"_"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                                 obj = {
                                        "type": '4x4',
                                        "task": ms["task"],
                                        "imageType": 'partial',
                                        "collectionName": collectionName,
                                        "path": ""
                                        }
                                 new.create_collection("collection")
                                 new.create_post(obj)
                                 new.create_collection(collectionName) 
                                 try:                           
                                         for ixx, fx in enumerate(list(HD.file.keys())[:]):
                                                   #print ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSos")
                                                   file_n = HD.file[fx][0]
                                                   try:
                                                      
                                                      answ_H = HD.file[fx][1]
                                                      #print ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSos", answ_H)
                                                   except IndexError:
                                                      answ_H = ""

                                                   iop = cv2.imread(file_n)
                                                   #print ("POST V")
                                                   answ_V = ViPost(file_n, str(ixx), ms["task"], int(ms["type"]))
                                                   post_s = {"file": file_n, "_type":ms["type"], "_task":ms["task"],
                                                             "answ": "", "answ_H": answ_H,
                                                             "answ_L" : "", "answ_V": answ_V["text"]}
		                                           #"answ": "", "answ_V": "", "task":ms["task"], "type":ms["type"]}
		                                           #"answ_L" : answ_L["text"], "answ_V": "1", "task":ms["task"]}
                                                   ixx = new.create_post(post_s)
                                                   #print ("End", ixx, post_s)
                                                   #I = new.posts.insert_one(post).inserted_id
                                 except KeyboardInterrupt:
                                                 print ("open")
                                                 pass
                                 temp_list = new.see_all_post()
                                 
                                 im_w = len(temp_list)
                                 print ("START", temp_list, im_w)
                                 w = im_w//10
                                 print ("START", temp_list, im_w, w)
                                 w_num = int(im_w/w)
                                 num = 0 
                                 for ix in range(0, w_num):
                                       f_list = temp_list[ix*w:(ix+1)*w]
                                       x = threading.Thread(target=thread_function, args=(new,ix, f_list, temp_list, ms["task"]))
                                       x.start()
                                 self.write_message(json.dumps({"Process": "loaddone"}))
                                                                                                                                   


                                     
                 ##############              
                #### VISUAL ####
                 ##############
                if list(ms.keys())[0] == "SeeAllData":
                      if ms["SeeAllData"] == "ProcessPrep":
                                    print ("All work", ms)
                                    new.create_collection("collection")
                                    list_coll = new.see_all_post()#see_collection() 
                                    obj = {"list":list_coll, "Process":"ProcessPrep"}
                                    #------->
                                    #new.create_collection("namesArch_8") # выбор 
                                    #new.see_all_post() # показать запеси
                                    #------->
                                    
                                    self.write_message(json.dumps(obj))
                                    
                      if ms["SeeAllData"] == "ProcessPick":              
                                    print ("Pick")
                                    new.create_collection(ms["collection_id"])
                                    self.temp_data = new.see_all_sort_post()
                                    print ("DATA Size",len(self.temp_data))
                                    self.temp_idx_s = 0
                                    self.temp_idx_f = 16
                      if ms["SeeAllData"] == "ProcessNext":
#                                      try:
#                                        if len(ms["idxx"]) == 16:
#                                          s_b = self.temp_idx_s
#                                          f_b = self.temp_idx_f
#                                          s_b -= 16
#                                          f_b -= 16
#                                          #print ("SEE", ms)
#                                          for mx, m in enumerate(ms["idxx"]):
#                                             posttoCH = new.see_post(ObjectId(m))
#                                             if int(ms["answ_v"][mx]) == 1:
#                                                  posttoCH["answ_V"] = [1]
#                                                  posttoCH["answ_L"] = [1]
#                                                  self.temp_data[s_b:f_b][mx]["answ_V"] = [1]
#                                                  self.temp_data[s_b:f_b][mx]["answ_L"] = [1]
#                                             if int(ms["answ_v"][mx]) == 0:
#                                                  posttoCH["answ_V"] = [0]
#                                                  posttoCH["answ_L"] = [0]
#                                                  self.temp_data[s_b:f_b][mx]["answ_V"] = [0]
#                                                  self.temp_data[s_b:f_b][mx]["answ_L"] = [0]
#                                             new.upd_post(ObjectId(m), posttoCH)
#                                        else:
#                                          t_4ix = self.temp_4idx
#                                          t_4ix -= 1
#                                          self.temp_data[t_4ix]["answ_V"] = deansw(ms["answ_v"])
#                                          posttoCH = new.see_post(ObjectId(ms["idxx"]))
#                                          posttoCH["answ_V"] = deansw(ms["answ_v"])
#                                          posttoCH["answ_L"] = deansw(ms["answ_v"])
#                                          new.upd_post(ObjectId(ms["idxx"]), posttoCH)
#                                      except KeyError:
#                                          pass
                                      try:
                                              if len(self.temp_data) != 0:
                                                   if int(self.temp_data[0]['_type']) < 4: 
                                                      im_w = len(self.temp_data)
                                                      w = 16
                                                      w_num = int(im_w/w)
                                                      k_id = []
                                                      l_data = []
                                                      k_answ = []
                                                      task = 0
                                                      for iox, op in enumerate(self.temp_data[self.temp_idx_s:self.temp_idx_f]):
                                                              print (op)
                                                              iop = cv2.imread(op["file"])
                                                              l_data.append(iop)
                                                              k_id.append(str(op['_id']))
                                                              if op["answ_V"] == [1] or op["answ_L"] == [1] or op["answ_H"] == [1]:
                                                                 k_answ.append(iox+1)
                                                              task = op['_task']
                                                      iop = newimg(np.array(l_data),4)
                                                      s = base64.b64encode(imgbite(iop))
                                                      obj = {"image":s.decode('ascii'), 
                                                                "answ_V": k_answ, 
                                                                "answ": "",
                                                                "task": task,
                                                                "type":4,
                                                                "_id": k_id,
                                                                "name": "",
                                                                "temp_idx_s":self.temp_idx_s,            
                                                                "temp_idx_f ":self.temp_idx_f }
                                                      self.temp_idx_s += 16
                                                      self.temp_idx_f += 16
                                                      self.write_message(json.dumps(obj))
                                                   else:
                                                   
                                                              iop = cv2.imread(self.temp_data[self.temp_4idx]["file"])
                                                              s = base64.b64encode(imgbite(iop))
                                                              idxx = self.temp_data[self.temp_4idx]["_id"]
                                                              fname = self.temp_data[self.temp_4idx]["file"]
                                                              answ_v = self.temp_data[self.temp_4idx]["answ_V"]
                                                              answ_l = self.temp_data[self.temp_4idx]["answ_L"]
                                                              answ_h = self.temp_data[self.temp_4idx]["answ_H"]
                                                              answ = self.temp_data[self.temp_4idx]["answ"] 
                                                              task = self.temp_data[self.temp_4idx]["_task"] 
                                                              tp = self.temp_data[self.temp_4idx]["_type"] 
                                                              #print (fname, idxx, task, tp)     
                                                              #print (">>>>>>>>>",answ_v, answ_h, answ_l, answ) 
                                                              l_t_a = []
                                                              for m in range(16):
                                                                  l_t_a.append(0)
                                                                  dix = m+1
                                                              #print ("><><><><><><><><>", len(l_t_a))
                                                              for msss, sh in enumerate(l_t_a):  
                                                                  
                                                                  #print ("><><><><>",dix, l_t_a[dix],len(l_t_a),"<><><><>") 
                                                                  dix = msss+1 
                                                                  if dix in answ_v:
                                                                     l_t_a[msss] = 1
                                                                  if dix in answ_l:
                                                                     l_t_a[msss] = 1
                                                                  if dix in answ_h:
                                                                     l_t_a[msss] = 1
                                                                  
                                                                  #print ("EEEE",l_t_a)
                                                              newassss = deansw(l_t_a)
                                                              print ("<<<<<<<<",newassss, len(l_t_a))          
                                                              s = base64.b64encode(imgbite(iop))
#                                                              obj = {"image":s.decode('ascii'), 
#                                                                        "answ_V": answ_v, 
#                                                                        "answ": answ,
#                                                                        "task": task,
#                                                                        "type":tp,
#                                                                        "_id": str(idxx),
#                                                                        "name": fname}
                                                              obj = {"image":s.decode('ascii'), 
                                                                        "answ_V": newassss, 
                                                                        "answ": answ,
                                                                        "task": task,
                                                                        "type":tp,
                                                                        "_id": str(idxx),
                                                                        "name": fname}
                                                                        
                                                              self.temp_4idx += 1
                                                              self.write_message(json.dumps(obj))   
                                                              
                                                                                                              
                                      except IndexError:
                                                    if int(self.temp_data[0]['_type']) < 4:    
                                                      self.temp_idx_s = 0
                                                      self.temp_idx_f = 16 
                                                      im_w = len(self.temp_data)
                                                      w = 16
                                                      w_num = int(im_w/w)
                                                      k_id = []
                                                      l_data = []
                                                      k_answ = []
                                                      task = 0
                                                      for iox, op in enumerate(self.temp_data[self.temp_idx_s:self.temp_idx_f]):
                                                              iop = cv2.imread(op["file"])
                                                              l_data.append(iop)
                                                              k_id.append(str(op['_id']))
                                                              if op["answ_V"] == [1] or op["answ_L"] == [1]:
                                                                 k_answ.append(iox+1)
                                                              task = op['_task']
                                                      iop = newimg(np.array(l_data),4)
                                                      s = base64.b64encode(imgbite(iop))
                                                      obj = {"image":s.decode('ascii'), 
                                                                "answ_V": k_answ, 
                                                                "answ": "",
                                                                "task": task,
                                                                "type":4,
                                                                "_id": k_id,
                                                                "name": "",
                                                                "temp_idx_s":self.temp_idx_s,            
                                                                "temp_idx_f ":self.temp_idx_f }
                                                      self.temp_idx_s += 16
                                                      self.temp_idx_f += 16
                                                      self.write_message(json.dumps(obj))
                                                    else:
                                                              self.temp_4idx = 0
                                                              iop = cv2.imread(self.temp_data[self.temp_4idx]["file"])
                                                              s = base64.b64encode(imgbite(iop))
                                                              idxx = self.temp_data[self.temp_4idx]["_id"]
                                                              fname = self.temp_data[self.temp_4idx]["file"]
                                                              answ_v = self.temp_data[self.temp_4idx]["answ_V"]
                                                              answ = self.temp_data[self.temp_4idx]["answ"] 
                                                              task = self.temp_data[self.temp_4idx]["_task"] 
                                                              tp = self.temp_data[self.temp_4idx]["_type"]      
                                                              s = base64.b64encode(imgbite(iop))
                                                              obj = {"image":s.decode('ascii'), 
                                                                        "answ_V": answ_v, 
                                                                        "answ": answ,
                                                                        "task": task,
                                                                        "type":tp,
                                                                        "_id": str(idxx),
                                                                        "name": fname}
                                                                        
                                                              self.write_message(json.dumps(obj))  





    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("index.html", title="Нейронная сеть/Тренировка")


class MainUpload(tornado.web.RequestHandler):
    def get(self):
        items = {}
        for x in mgDC:
           #J = list(new.posts.find({"task": x}))
           items[x] = 0#len(J)
        self.render("upload.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))


class MainData(tornado.web.RequestHandler):
    def get(self):
       self.render("data1.html", title="Нейронная сеть/Тренировка")


class record():
     def __init__(self, x):
         self.file = open(x+'.csv', 'w')
         #print "LOAD"

     def toDown(self, x):
         try:
            os.mkdir(x)
         except OSError:
            for fl in  os.listdir(x):
                file_path = os.path.join(x, fl)
                if os.path.isfile(file_path):
                   os.remove(file_path)
            os.rmdir(x)
            os.mkdir(x)
     def cop(self, x, y):
         f_file = open(x, "rb").read()
         to_file = open(y,"wb").write(f_file)
     def save_one(self, x, y):
         self.file.write("{};{};\n".format(x, y))
 
     def save(self, x):
         self.file.write("{};{};\n".format(x["file"].split("/")[-1], [int(f) for f in x["answ_V"]]))
         #self.file.write("{};answV:{};answL:{};answH:{};answ{};task:{};\n".format(x["file"].split("/")[-1],
         #                                                                               [int(f) for f in x["answ_V"]],
         #                                                                               x["answ_L"],
         #                                                                               x["answ_H"], 
         #                                                                               x["answ"],
         #                                                                               x["_task"])) 
#{};answ_v:{};answ_l:{};answ_new_human:{};answ_human:{};task:{}

def tardir(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file))


#def LLK(i):
#        aJNEW = [] 
#        aJL = []
#        aJV = [] 
#        
#        for ix, x in enumerate(i):
#          if int(x["_type"]) == 3 or int(x["_type"]) == 1:
#             if x["answ_V"] == [1]:
#                aJV.append(x)#[ix] = x["answ_V"]
#             if x["answ_L"] == [1]:
#                aJL.append(x)
#             if x["answ_L"] == x["answ_V"]:
#                if x["answ_V"] == [1]: 
#                   aJNEW.append(x)             
#          else:
#             if x["answ_V"] != []:
#                aJV.append(x)
#             if x["answ_L"] != []:
#                aJL.append(x)
#             if x["answ_L"] == [int(h) for h in x["answ_V"]]:
#                aJNEW.append(x)
#                
#        return aJNEW, aJV, aJL
def LLK(i):
        answ_LV = [] 
        answ_L = []
        answ_V = []
        answ_H = [] 
        answ_LH = []
        
        
        for ix, x in enumerate(i):
          if int(x["_type"]) == 3 or int(x["_type"]) == 1:
             if x["answ_V"] == [1]:
                answ_V.append(x)#[ix] = x["answ_V"]
             if x["answ_L"] == [1]:
                answ_L.append(x)
             if x["answ_H"] == [1]:
                answ_H.append(x)                
             if x["answ_L"] == x["answ_V"]:
                if x["answ_V"] == [1]: 
                   answ_LV.append(x) 
             if x["answ_L"] == x["answ_H"]:
                if x["answ_L"] == [1]: 
                   answ_LH.append(x)             
          else:
             if x["answ_V"] != []:
                answ_V.append(x)
             if x["answ_L"] != []:
                answ_L.append(x)
             if x["answ_H"] != []:
                answ_H.append(x)                    
             if x["answ_L"] == [int(h) for h in x["answ_V"]]:
                answ_LV.append(x)
                
        return answ_LV, answ_V, answ_L, answ_H, answ_LH


##
class MainLoad(tornado.web.RequestHandler):
    
    def get(self):
           items = {}
        #for x in mgDC["4x4"]:
           #J = list(new.posts.find({"_task": x}))
           new.create_collection("collection")
           list_coll = new.see_all_post()#see_collection() 
           #J = see_all_post()
           for x in range(len(list_coll)):
               #print (list_coll[x])
               new.create_collection(list_coll[x]['collectionName'])
               list_coll_temp = new.count()
               
               items[list_coll[x]['collectionName']] = list_coll_temp
           self.render("load.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))
    def post(self):
        data_json = json.loads(self.request.body) 
        if data_json["st"] == "prep":

                new.create_collection(data_json['task'])
                list_coll_temp = new.see_all_post()
                Gg = LLK(list_coll_temp)
#                print ("POST", len(Gg[0].keys()),len(Gg[1].keys()), len(Gg[2].keys()))#self.request.body #Gg
#                """Готовим статистику""" 
                kolo = {"answ":len(list_coll_temp),"LV":len(Gg[0]), "answ_L":len(Gg[2]) , "answ_V":len(Gg[1]), "answ_H":len(Gg[3]), "LH":len(Gg[4])} 
                self.write(kolo)
        else:
                print (data_json)#["task"]
                new.create_collection(data_json['task'])
                list_coll_temp = new.see_all_post()
                Gg = LLK(list_coll_temp)
                for ix, x in enumerate(Gg[1]):
                    print (ix, x)
                    if int(x["_type"]) == 1:
                         rec.save_one(x[k]["file"],x[k]["answ_V"])
                    else:
                         rec.save(x)
                kolo = {"csv":'temp_csv/'+data_json["task"]+'.csv'}
                self.write(kolo)                         
#                         
#                """create load"""
#                rec = record('temp_csv/'+data_json["task"])
#                #rec.toDown('temp/'+data_json["task"])
#                for ix, x in enumerate(new.posts.find({ "_task": data_json["task"]})):
#                   if int(x["_type"]) == 1:
#                   #print (x)
#                     for k in list(x.keys())[3:]:
#                
#                       if int(x[k]["answ_V"]) == 1:
#                          #print (x[k]["file"],x[k]["answ_V"])
#                          rec.save_one(x[k]["file"],x[k]["answ_V"])
#                   else:
#                       rec.save(x)
#                         
#                #kolo = {"csv":'temp_csv/'+data_json["task"]+'.csv' , "arch":'to_load/'+data_json["task"]+'.tar.gz' }
#                kolo = {"csv":'temp_csv/'+data_json["task"]+'.csv'}
#                self.write(kolo)





app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", MainUpload),
        (r"/alldata", MainData),
        (r"/load", MainLoad),
        (r"/websocket", ImageWebSocket),
        (r"/(robots-AI.jpg)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(index.png)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path':'./', 'default_filename': 'index.html'}),
    ])
app.listen(8800)


tornado.ioloop.IOLoop.current().start()

"""
временная колекци
ответ людей отрицательный нет искомого класса
ответ леонида отрицательный нет искомого обьекта
 ответ люжейц ролдлжительный искомый обьект
 сравнить там где разошлись положительный ответ людей с леонидом

Каждый раз


Убираю сортировку по папкам - только csv и картинки - 
В архиве 23, no_23, и всякое такое к чему не готовил сервис!





В некоторых 3 папки - получается что лучше делать csv и папки
Выберите класс - выбрать класс искомого обьекта
Выберите тип - 4x4 - храниться в бд целой картинкой
               3x3 - храниться в бд разрезанной
               1x1 - храняться без обработки - как части 3x3
               ничего не выбрано - храняться без обработки - как части 3x3



Загрузка 3x3 разрезаю и складываю в одну папку ( в эту папку отправляю 1x1 )
Загрузка 4x4 складываю в папку целых

Создаю бд для каждого архива

Добрый день, есть желание реализовать 2 проекта в течении своей жизни, вы можете помочь?
По каждому из вариантов есть мысли и детальные шаги реализации:

1 | собрать медецинскую базу лекарств и их химические свойства.
Эффективность лекарст для каждого восраста,болезни, создать базу цен:
  а) из интернет источников по положительным и отрицательным отзывам
  б) собрать отзывы врачей
  в) данные анализов и влияние на них лекарств
Обработать данные нейронной сетью и получить приложение способное составлять рецепт эффективных
лекарств в зависемости от ваших биологических показателей и болезни

2 | Перенос сознания
Начать с обучения бота в игре gta 5
Научиться управлять ботом с помощью силы мысли

Перенести бота в автомобиль ВАЗ 2121, проверить работоспособность
Управление ВАЗ 2121 с помощью мысли

Начать эксперемент по переносу сознания:
Конечный эксперемент - подключить двухсторонний датчик
к спящему человеу и обученной модели - задать вопрос алгоритму
Цель алгоритма донести задаваемый вопрос спящему в другой комнате человек
Если испытуемый после сна сможет воспроизвести вопрос - считать эксперемент удачным!

"""


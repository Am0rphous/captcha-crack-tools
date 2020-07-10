# -*- coding: utf-8 -*-
from pymongo import MongoClient
from tornado.escape import json_encode
from bson.objectid import ObjectId
from tornado.escape import json_encode

import cv2
import numpy as np
import os, sys, io
import shutil
import glob, base64, json, time

from zipfile import ZipFile
import tarfile
import requests

import tornado.ioloop
import tornado.web
import tornado.websocket

from data_base import mDB
from data_post_nn import *
from data_parsing import DATA


#4x4:
#mountains
#palms
#hydrants
#buses
#crosswalks
#traffic_lights
#chimneys
#stairs
#motorbike
#bicycles
#tractors
#taxi
#bridges


#3x3/2x4:
#cars
#stores
#bridges
#vehicles
#buses3
#traffic_lights3
#crosswalks3
#boats3
#bicycles3
#taxi3
#sculptures3
#motos3
#hydrants3
#tractors3
#chimneys3
#stairs3
#trees3


mgDC = [["mountains",
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
        "bridges"], ["cars",
                     "stores",
                     "bridges",
                     "vehicles",
                     "buses3",
                     "traffic_lights3",
                     "crosswalks3",
                     "boats3",
                     "bicycles3",
                     "taxi3",
                     "sculptures3",
                     "motos3",
                     "hydrants3",
                     "tractors3",
                     "chimneys3",
                     "stairs3",
                     "trees3"]]
                    

"""
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
               "bridges", "boats", "sculptures", "trees"]
"""
# База данных

new = mDB()  



def deansw(x):
    s = []
    for ix, i in enumerate(x):
        if i == 1:
           s.append(ix+1)
    return s


#def ViPost(x, idx, task, c_box):
#    url = "http://178.158.131.41:9900/"
#    with open(x, "rb") as f:
#            data = f.read()
#            data = base64.b64encode(data).decode('utf-8')
#            payload = {"image":data, "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task, "c_box": c_box }
#            headers = { 'Content-Type': "application/json",
#                        'cache-control': "no-cache" }
#            response = requests.request("POST", url, data=json_encode(payload), headers=headers)
#            return json.loads(response.text)
#            
#def cutimg(name, data, idx, answ, task, col, collectionName):
#	if True:
#                im_w, im_h, im_c = data.shape
#                w, h = im_w//col, im_h//col
#                w_num, h_num = int(im_w/w), int(im_h/h)
#                num = 0
#                ls = []
#                try: 
#                        #print "post>"
#                        for wi in range(0, w_num):
#                           for hi in range(0, h_num):
#                                num += 1
#                                y = "data/"+ collectionName + "/"+str(num)+str(idx)+"_"+name.split("/")[-1]
#                                cv2.imwrite(y, data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
#                                if num in answ:
#                                   post_s = {"file": y, "_type":col, "_task":task,
#                                           "answ": "", "answ_H": "",
#                                           "answ_L" : "", "answ_V": [1]}
#                                   ls.append(post_s)
#                                else:
#                                   post_s = {"file": y,  "_type":col, "_task":task,
#                                             "answ": "", "answ_H": "",
#                                             "answ_L" : "", "answ_V": [0]}
#                                   ls.append(post_s)

#                        return ls
#                except IndexError: 
#                   pass 

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
                      try:
                        imzero[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :] = data[num]
                        num += 1
                      except IndexError:
                        imzero[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :] = np.zeros(shape=(100, 100, 3), dtype=np.uint8)

                return imzero



def cutimg(name, data, idx, task, col, collectionName):
                im_w, im_h, im_c = data.shape
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
                ls = []
                try: 
                        for wi in range(0, w_num):
                           for hi in range(0, h_num):
                                num += 1
                                y = "data/"+ collectionName + "/"+str(num)+str(idx)+"_"+name.split("/")[-1]
                                cv2.imwrite(y, data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                                post_s = {"file": y, "_type":col, "_task":task,
                                          "answ": "", "answ_H": "",
                                          "answ_L" : "", "answ_V": ""}
                                ls.append(post_s)

                        return ls
                except IndexError: 
                   pass 
                   

def sort_list_send(ms, temp_data, list_data):
                                    if int(ms["type"]) != 4:
                                            try:
                                                    if ms['SortType'] == "H":
                                                            for i in temp_data:
                                                               if i['answ'] != "":
                                                                 if i['answ_H'] != i['answ_L']:# == [1]:
                                                                     if i['answ_H'] == [1]:
                                                                        list_data.append(i)
                                                    if ms['SortType'] == "L":
                                                            for i in temp_data:
                                                               if i['answ'] != "":
                                                                 if i['answ_H'] != i['answ_L']:# == [1]:
                                                                     if i['answ_L'] == [1]:
                                                                        list_data.append(i)  
                                            except KeyError:
                                                    for i in temp_data:  
                                                        list_data.append(i) 
                                    else:
                                            #print ("4ssss")
                                            try:
                                                    if ms['SortType'] == "H":
                                                            for i in temp_data:
                                                               if i['answ'] != "":
                                                                 if i['answ_H'] != i['answ_L']:# == [1]:
                                                                     if i['answ_H'] != "":
                                                                        list_data.append(i)
                                                    if ms['SortType'] == "L":
                                                            for i in temp_data:
                                                               if i['answ'] != "":
                                                                 if i['answ_H'] != i['answ_L']:# == [1]:
                                                                     if i['answ_L'] != "":
                                                                        list_data.append(i)  
                                            except KeyError:
                                                    for i in temp_data:  
                                                        list_data.append(i) 



    



class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    myfile = 0
    seeidx = 0
    name = "" 
    tempID = 0 
    temp_data = [] 
    list_data = []
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
                   #"""Конец загрузки"""

                           self.myfile.close()
                           HD = DATA()
                           lss = ["gz", "tar", "xz"]
                           collectionName = self.name+"_"+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())  
                           if self.name.split(".")[-1] in lss:
                                   tar = tarfile.open("archiv/"+self.name, "r")
                                   tar.extractall("data/"+collectionName)#, members=self.track_progress(tar))
                                   tar.close()

                           if self.name.split(".")[-1] == "zip":
                                   zip = ZipFile("archiv/"+self.name)
                                   zip.extractall("data/"+collectionName)
                                   
                           HD.parseIMG(collectionName)
                           try:
                               HD.parseCSV()
                           except:
                               pass
                                   
                           obj = {
                                        "type": ms["type"]["type"],
                                        "task": ms["task"],
                                        "imageType": 'original',
                                        "collectionName": collectionName,
                                 }
                           # добавляю в колекцию      
                           new.create_collection("collection")
                           new.create_post(obj)
                           # создаю колекцию
                           new.create_collection(collectionName)
                           print ("RAR", ms["type"])
                           #for h in ms["type"]:
                           if ms["type"]["L"] == "" or ms["type"]["V"] == "":    
                                   if int(ms["type"]["type"]) == 3:
                                         try: 
                                                 for ixx, fx in enumerate(list(HD.file.keys())[:]):
                                                           file_n = HD.file[fx][0]
                                                           try:
                                                              answ_H = HD.file[fx][1]
                                                           except IndexError:
                                                              answ_H = ""

                                                           iop = cv2.imread(file_n)
                                                           #answ_V = ViPost(file_n, str(ixx), ms["task"], int(ms["type"])) 
                                                           
                                                           PP = cutimg(file_n, iop, ixx, ms["task"], int(ms["type"]["type"]), collectionName)
                                                           
                                                           ixx = new.create_many(PP)
                                         except KeyboardInterrupt:
                                                         print ("open")
                                                         pass                                   
                                   else:
                                           try:   
                                                         for ixx, fx in enumerate(list(HD.file.keys())[:]):
                                                                   file_n = HD.file[fx][0]
                                                                   try:
                                                                      answ_H = HD.file[fx][1]
                                                                   except IndexError:
                                                                      answ_H = ""
                                                                   if int(ms["type"]["type"]) == 1:
                                                                           if file_n.split("/")[-2].split("_")[0]=="not":
                                                                              answ_H = [0]
                                                                           else:
                                                                              answ_H = [1]
                                                                   post_s = {"file": file_n, "_type":ms["type"]["type"],
                                                                             "_task":ms["task"],
                                                                             "answ": "", "answ_H": answ_H,
                                                                             "answ_L" : "", "answ_V": ""}
                                                                   ixx = new.create_post(post_s) #

                                           except KeyboardInterrupt:
                                                         print ("open")
                                                         pass
                                   print ("END", ms)        
                                   self.write_message(json.dumps({"Process": "loaddone"}))
                           #######################
                          ###   1 x 1 #############
                           ####################### 
                if list(ms.keys())[0] == "ProcessPrep":
                                    new.create_collection("collection")
                                    list_coll = new.see_all_post()#see_collection() 
                                    obj = {"list":list_coll, "Process":"ProcessPrep"}
                                    self.write_message(json.dumps(obj))
                        
                        
                 ##############              
                #### DELITE ####
                 ##############                        
                                    
                if list(ms.keys())[0] == "Delite":
                                    print ("Delite", ms["idxx"])
                                    new.create_collection("collection")
                                    new.del_one_post(ObjectId(ms["idxx"]))
                                    #------->
                                    new.create_collection(ms["C_name"])
                                    new.del_collection()
                                    
                 ################              
                #### GET ANSW ####
                 ################ 
                                    
                if list(ms.keys())[0] == "GetAns":  
                                 new.create_collection("collection")
                                 se_post = new.see_post(ObjectId(ms["idxx"]))
                                 
                                 new.create_collection(ms["C_name"])
                                 temp_list = new.see_all_post()
                                 print ("GetAns", ms, len(temp_list), se_post)
                                 im_w = len(temp_list)
                                 w = im_w//20
                                 w_num = int(im_w/w)
                                 num = 0 
                                 threads = []
                                 for ix in range(0, w_num):
                                       f_list = temp_list[ix*w:(ix+1)*w]
#                                       if se_post["task"] != "cars":
#                                          T_task = se_post["task"]+"3"
#                                       else:
#                                          T_task = se_post["task"]
                                       if se_post["task"] != "cars":
                                          T_task = se_post["task"]#[:-1]
                                       else:
                                          T_task = se_post["task"]
                                       print (T_task)
                                       x = threading.Thread(target=thread_function, args=(new,ix, f_list, temp_list, T_task))
                                       threads.append(x)
                                       x.start()
                                       
                                 flag =1
                                 while (flag):
                                         for t in threads:
                                            if t.isAlive():
                                               flag = 1
                                            else:
                                               flag = 0
                                               print ("Final")
                                               self.write_message(json.dumps({"GetAns":"Final"}))
                 ##############              
                #### VISUAL ####
                 ##############
                if list(ms.keys())[0] == "SeeAllData":
                      if ms["SeeAllData"] == "ProcessStat": 
                      
                                    new.create_collection(ms["collection_id"])
                                    s_len = new.count()
                                    if int(ms["type"]) != 4:
                                            s_stat = new.stat()
                                            obj = {"all_len":s_len, "ans_v_len":s_stat[0],  "ans_l_len":s_stat[1], "ans_h_len":s_stat[2], "ans_len":s_stat[3], "Process":"Stat", "collection":ms["collection_id"], "type":ms["type"]} #
                                            
                                            new.create_collection(ms["collection_id"])
                                            self.temp_data = new.see_sort() #see_all_post()
                                            self.temp_idx_s = 0
                                            self.temp_idx_f = 16
                                            self.write_message(json.dumps(obj))
                                    else:
                                            self.temp_data = new.see_all_post()
                                            s_stat = new.stat4()
                                            obj = {"all_len":s_len, "ans_v_len":s_stat[0],  "ans_l_len":s_stat[1], "ans_h_len":s_stat[2], "ans_len":s_stat[3], "Process":"Stat", "collection":ms["collection_id"], "type":ms["type"]} #  
                                            self.write_message(json.dumps(obj))  
                                    #print ("Pick DATA",len(self.temp_data), ms)
                                                                   
                      if ms["SeeAllData"] == "ProcessPick": 
                                    self.list_data = []
                                    sort_list_send(ms, self.temp_data, self.list_data)
                                                                                                        
                                    #self.temp_data = lists           
                                    print (">>>", ms, len(self.list_data))              
                                    
                      if ms["SeeAllData"] == "ProcessNext":
                                      
                                      try:
                                        if type(ms["idxx"]) == list:
                                          #print ("ERRROR THIS", ms)
                                          s_b = self.temp_idx_s
                                          f_b = self.temp_idx_f
                                          s_b -= 16
                                          f_b -= 16
                                          #print ("SEE", ms)
                                          for mx, m in enumerate(ms["idxx"]):
                                             posttoCH = new.see_post(ObjectId(m))
                                             if int(ms["answ_v"][mx]) == 1:
                                                  posttoCH["answ"] = [1]
                                                  self.list_data[s_b:f_b][mx]["answ"] = [1]
                                             if int(ms["answ_v"][mx]) == 0:
                                                  posttoCH["answ"] = [0]
                                                  self.list_data[s_b:f_b][mx]["answ"] = [0]
                                             new.upd_post(ObjectId(m), posttoCH)
                                        else:
                                          
                                          t_4ix = self.temp_4idx
                                          t_4ix -= 1
                                          self.list_data[t_4ix]["answ_V"] = deansw(ms["answ_v"])
                                          posttoCH = new.see_post(ObjectId(ms["idxx"]))
                                          posttoCH["answ"] = deansw(ms["answ_v"])
                                          new.upd_post(ObjectId(ms["idxx"]), posttoCH)
                                      except KeyError:
                                          pass
                                      if len(self.list_data) != 0:
                                                                                              
                                                   if int(self.list_data[0]['_type']) < 4: 
                                                        
                                                              im_w = len(self.list_data)
                                                              print (im_w,self.temp_idx_s, self.temp_idx_f)
                                                              w = 16
                                                              #w_num = int(im_w/w)
                                                              
                                                              k_id = []
                                                              list_answ = []
                                                              l_data = []
                                                              k_answ = []
                                                              task = 0
                                                              for iox, op in enumerate(self.list_data[self.temp_idx_s:self.temp_idx_f]):
                                                                      #print (op)
                                                                      iop = cv2.imread(op["file"])
                                                                      l_data.append(iop)
                                                                      k_id.append(str(op['_id']))
                                                                      if op["answ_V"] == [1] or op["answ_L"] == [1] or op["answ_H"] == [1]:
                                                                         k_answ.append(iox+1)
                                                                      list_answ.append(op)
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
                                                                        "list_answ":list_answ,
                                                                        "temp_idx_s":self.temp_idx_s,            
                                                                        "temp_idx_f":self.temp_idx_f,
                                                                        "all_len_work":im_w,
                                                                        }
                                                              self.temp_idx_s += 16
                                                              self.temp_idx_f += 16
                                                              
                                                              self.write_message(json.dumps(obj))

                                                   else:
                                                              print (len(self.list_data) , self.temp_4idx, self.temp_idx_s, self.temp_idx_f)
                                                              iop = cv2.imread(self.list_data[self.temp_4idx]["file"])
                                                              s = base64.b64encode(imgbite(iop))
                                                              idxx = self.list_data[self.temp_4idx]["_id"]
                                                              fname = self.list_data[self.temp_4idx]["file"]
                                                              answ_v = self.list_data[self.temp_4idx]["answ_V"]
                                                              answ_l = self.list_data[self.temp_4idx]["answ_L"]
                                                              answ_h = self.list_data[self.temp_4idx]["answ_H"]
                                                              answ = self.list_data[self.temp_4idx]["answ"] 
                                                              task = self.list_data[self.temp_4idx]["_task"] 
                                                              tp = self.list_data[self.temp_4idx]["_type"] 
                                                              #print (fname, idxx, task, tp)     
                                                              #print (">>>>>>>>>",answ_v, answ_h, answ_l, answ) 
                                                              l_t_a = []
                                                              for m in range(16):
                                                                  l_t_a.append(0)
                                                                  dix = m+1
                                                              for msss, sh in enumerate(l_t_a):  
                                                                  dix = msss+1 
                                                                  
#                                                                  if dix in answ_v:
#                                                                     l_t_a[msss] = 1
#                                                                  if dix in answ_l:
#                                                                     l_t_a[msss] = 1
                                                                  if dix in answ_h:
                                                                     l_t_a[msss] = 1
                                                              newassss = deansw(l_t_a)
                                                              s = base64.b64encode(imgbite(iop))
                                                              obj = {"image":s.decode('ascii'), 
                                                                        "answ_V": newassss, 
                                                                        "answ": answ,
                                                                        "list_answ":self.list_data[self.temp_4idx],
                                                                        "task": task,
                                                                        "type":tp,
                                                                        "_id": str(idxx),
                                                                        "temp_idx":self.temp_4idx,
                                                                        "all_len_work":len(self.list_data),
                                                                        "name": fname}
                                                                        
                                                              self.temp_4idx += 1
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
        for ix, x in enumerate(mgDC):
           #J = list(new.posts.find({"task": x}))
           #items[x] = len(x)
           t = {}
           for i in x:
              t[i] = i
           items[ix] = t  
        #print (items) 
        self.render("upload.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))


class MainData(tornado.web.RequestHandler):
    def get(self):
       self.render("data.html", title="Нейронная сеть/Тренировка")




"""
Создаю POST
получить все классы с типом 1x1/3x3 

"""
##
class record():
     def __init__(self):
         #self.file = open(x+'.csv', 'w')
         print ("LOAD")

     def csv_c(self, x):
         self.file = open(x+'.csv', 'w')
         
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
     def delTemp(self, x):  
         try:
                 path = os.path.join(os.path.abspath(os.path.dirname(__file__)), x)  
                 shutil.rmtree(path)  
                 os.mkdir(x)
         except:
                 os.mkdir(x)       
     def cop(self, x, y):
         f_file = open(x, "rb").read()
         to_file = open(y,"wb").write(f_file)
     def save_one(self, x, y0, y1, y2, y3):
         self.file.write("{};{};{};{};{};\n".format(x, y0, y1, y2, y3))
     """
     def save(self, x):
         self.file.write("{};{};\n".format(x["file"].split("/")[-1], [int(f) for f in x["answ_V"]]))
     """
def tardir(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file))



class MainLoad(tornado.web.RequestHandler):
    
    def get(self):
        items = {}
        for x in mgDC:
           #J = list(new.posts.find({"task": x}))
           items[x] = x
        self.render("load.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))
    def post(self):
        data_json = json.loads(self.request.body) 
        print (data_json)
        if int(data_json["type"]) != 4:
                if data_json["st"] == "prep":
                        new.create_collection("collection")
                        list_coll_temp = new.see_all_post()
                        
                        list_to_load = []
                        for u in list_coll_temp:
                           print (u)
                           if u["task"] == data_json["task"]:
                             if int(u["type"]) == int(data_json["type"]) or int(u["type"])==1:
                                #print (data_json, list_coll_temp)
                                list_to_load.append(u)
                           
                        #print (list_to_load)
                        list_to = []
                        for u in list_to_load:
                            new.create_collection(u['collectionName'])
                            #list_coll_temp = new.see_all_post()
                            new.see_sort_load(list_to)
                            #print (len(list_coll_temp))
                            #list_to.append(list_coll_temp)
                        print (len(list_to))
                        _good = []
                        _bad = []
                        rec = record()
                        for u in list_to:
                            if u["answ_H"] == u["answ_L"] and u["answ_H"] == [1] or u["answ"] == [1]:
                               _good.append(u)
                            else:
                               _bad.append(u)
                        print (len(_good), len(_bad))   
                        
                        
                        rec.delTemp("temp")
                        
                        rec.toDown('temp/'+data_json["task"]) 
                        for u in _good:
                            rec.cop(u['file'], 'temp/'+data_json["task"] + "/" + u['file'].split("/")[-1])
                            
                        rec.toDown('temp/not_'+data_json["task"])     
                        for u in _bad:
                            rec.cop(u['file'], 'temp/not_'+data_json["task"] + "/" + u['file'].split("/")[-1])
                        
                        tardir('temp', data_json["task"]+'.tar.gz')
                        kolo = {"arch": data_json["task"]+'.tar.gz', "type": 1}
                        self.write(kolo)
        else:
                if data_json["st"] == "prep":
                        
                        new.create_collection("collection")
                        list_coll_temp = new.see_all_post()
                        list_to_load = []
                        #print ("4x4", list_coll_temp) 
                        for u in list_coll_temp:
                           if u["task"] == data_json["task"]:
                             if int(u["type"]) == int(data_json["type"]):
                                #print (data_json["type"], u)
                                list_to_load.append(u)
                        #print ("4x4", len(list_to_load), data_json["type"])        
                        list_to = []
                        for u in list_to_load:
                            new.create_collection(u['collectionName']) 
                            new.see_all_post4(list_to) 
                        print (len(list_to)) 
                        rec = record() 
                        rec.csv_c(data_json["task"]) 
                        
                        rec.delTemp("temp")
                        
                        rec.toDown('temp/'+data_json["task"])
                        for u in list_to:
                           #print (u)   
                           rec.cop(u['file'], 'temp/'+data_json["task"] + "/" + u['file'].split("/")[-1])
                           rec.save_one(u["file"].split("/")[-1], u["answ_H"], u["answ_L"], u["answ_V"], u["answ"])
                        #print ("END")
                        
                        tardir('temp', data_json["task"]+'.tar.gz') 
                        kolo = {"arch": data_json["task"]+'.tar.gz', "csv": data_json["task"]+'.csv', "type": 4}
                        self.write(kolo)





app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", MainUpload),
        (r"/alldata", MainData),
        (r"/load", MainLoad),
        (r"/websocket", ImageWebSocket),
        (r"/(robots-AI.jpg)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(index.png)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(pv_layer_controls.png)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path':'./', 'default_filename': 'index.html'}),
    ])
app.listen(8800)


tornado.ioloop.IOLoop.current().start()
"""
L == H, answ != 0,  
L == H, answ == 1 or answ == "":
9 428 14 242
9284 14386

"""


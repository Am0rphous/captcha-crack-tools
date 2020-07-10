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


mgDC = {"4x4":["mountains",
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
               "bridges"]}



class DATA(object):
        def __init__(self):
            self.file = {}
            self.csv = "";
            #self.parseIMG()
            #print self.file
            #try:
            #  self.parseCSV()
            #except IOError:
            #  pass
            
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
"""
def LeoPost(x, idx, task):
    url = "http://148.251.0.181:8084/"
    with open(x, "rb") as f:
            data = f.read()
            payload = {"image":data.encode("base64"), "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task}
            headers = { 'Content-Type': "application/json",
                        'cache-control': "no-cache" }
            response = requests.request("POST", url, data=json_encode(payload), headers=headers)
            return json.loads(response.text)
"""

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
        #print ix, i
        if i == 1:
           s.append(ix+1)
    return s

def cutimg(data, idx, task ,col):
        if col == 3:
                  if True:
                      ans = []
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
                               print (an)
                               ans.append(an['text'][0])
                               #imgs(i[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
		        #print ans
                      return deansw(ans)
        else:
                  return LeoPost(data, idx, task)





def ViPost(x, idx, task, c_box):
    url = "http://178.158.131.41:8800/"
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
                im_w, im_h, im_c = 400, 400, 3
                imzero = np.zeros(shape=(im_w, im_h, im_c), dtype=np.uint8)
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
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


class DB(object):
    def __init__(self):
        self.pyDB = MongoClient('localhost', 27017)
        self.db = self.pyDB.dynamic_one #dynamic#test#_database #database# 
        self.posts = self.db.posts  

new = DB()    

class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    myfile = 0
    seeidx = 0
    name = "" 
    ss = new.posts.find()
    tempID = 0    

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
                           if self.name.split(".")[-1] == "zip":
                                   zip = ZipFile("archiv/"+self.name)
                                   zip.extractall("data/"+self.name)
                           
                                   HD.parseIMG(self.name)
                           #print (HD.file, ms["type"] == 1)
                           if int(ms["type"]) != 1:
                                 for ixx, fx in enumerate(list(HD.file.keys())[:]):
		                           
                                           file_n = HD.file[fx][0]
                                           try:
                                              answ_H = HD.file[fx][1]
                                           except IndexError:
                                              answ_H = ""

                                           iop = cv2.imread(file_n)
                                           #print ("POST V")
                                           answ_V = ViPost(file_n, str(ixx), ms["task"], int(ms["type"]))#""#gg(iop, ms["task"], int(ms["type"]))                   
                                           #print (answ_V["text"],"POST L")
                                           #answ_L = cutimg(iop, str(ixx), ms["task"], int(ms["type"]))
		               
                                           #print (answ_L["text"]) #answ_V[0]
                                           #print (file_n, ms["task"], ms["type"]) #int(ms["type"]))
                                           post = {"file": file_n, 
                                                   "answ": "", "answ_H": answ_H, "_type":ms["type"],
                                                   "answ_L" : "", "answ_V": answ_V["text"], "_task":ms["task"]}
		                                   #"answ": "", "answ_V": "", "task":ms["task"], "type":ms["type"]}
		                                   #"answ_L" : answ_L["text"], "answ_V": "1", "task":ms["task"]}
                                           I = new.posts.insert_one(post).inserted_id

                                 self.ss = new.posts.find()
                                 self.write_message(json.dumps({"Process": "loaddone"}))
                           else:
                                 im_w = len(list(HD.file.keys()))
                                 w = 16
                                 w_num = int(im_w/w)
                                 num = 0
                                 #print ("ErrorS", im_w, w_num, w) 
                                 for ix in range(0, w_num): 
                                     #print (len(list(HD.file.keys())[ix*w:(ix+1)*w]))
                                     t_dict = {}
                                     t_dict["_type"] = ms["type"]
                                     t_dict["_task"] = ms["task"]
                                     for kix in list(HD.file.keys())[ix*w:(ix+1)*w]:
                                           #print (HD.file[kix],ix)
                                           file_n = HD.file[kix][0]
                                           post = {"file": file_n, 
                                                   "answ": "", "answ_H": "",
                                                   "answ_L" : "", "answ_V": "1"}
                                           t_dict[str(ix)+"_"+str(kix)] = post
                                     #print (len(list(t_dict.keys())))
                                     I = new.posts.insert_one(t_dict).inserted_id  
                                 self.ss = new.posts.find()
                                 self.write_message(json.dumps({"Process": "loaddone"}))
                                     
                                          


                if list(ms.keys())[0] == "SeeAllData":
                      if ms["SeeAllData"] == "ProcessNext":
                                      try:
                                          posttoCH = new.posts.find_one(ObjectId(ms["idxx"]))
                                          if posttoCH["_type"] == 1:
                                             for ik, k in enumerate(list(posttoCH.keys())[3:]):
                                                 posttoCH[k]["answ_V"] = ms["answ_v"][ik]
                                             new.posts.update_one({"_id" : ObjectId(ms["idxx"])},
                                                                  {"$set": posttoCH}, upsert=True)
                                          else:

                                             self.tempID = ObjectId(ms["idxx"])
                                             posttoCH = new.posts.find_one(ObjectId(ms["idxx"]))
                                             posttoCH["answ_V"] = deansw(ms["answ_v"])
                                             new.posts.update_one({"_id" : ObjectId(ms["idxx"])},
                                                                  {"$set": posttoCH}, upsert=True)
                                             #posttoCH = new.posts.find_one(ObjectId(ms["idxx"]))
       
                                      except KeyError:
                                          pass

                                      if new.posts.count() != 0:

                                              try:
                                                 obj = self.ss.next()
                                              except StopIteration:
                                                 self.ss.rewind()
                                                 obj = self.ss.next() 
                                              #print (obj["task"])
                                              if obj["_type"] == 1:
                                                 k_answ = []
                                                 l_data = []
                                                 ixxx = 0
                                                 #print (obj["_type"])
                                                 for k in list(obj.keys())[3:]:
                                                    n_file = obj[k]['file']
                                                    ixxx += 1
                                                    if int(obj[k]['answ_V']) == 1:
                                                       k_answ.append(ixxx)
                                                    iop = cv2.imread(n_file)
                                                    l_data.append(iop)
                                                 iop = newimg(np.array(l_data),4)   
                                                 idxx = obj["_id"]
                                                 answ_v = k_answ 
                                                 answ = k_answ 
                                                 task = obj["_task"]
                                                 #LeoPost(fname, str(idxx))
                                                 s = base64.b64encode(imgbite(iop))
                                                 obj = {"image":s.decode('ascii'), 
                                                        "answ_V": answ_v, 
                                                        "answ": answ,
                                                        "task": task,
                                                        "type":4,
                                                        "_id": str(idxx),
                                                        "name": ""}
                                                 #print (obj["type"])
                                                 self.write_message(json.dumps(obj))
                                              else:
                                                 try:
                                                   obj = self.ss.next()
                                                 except StopIteration:
                                                   self.ss.rewind()
                                                   obj = self.ss.next()    
                                                 idxx = obj["_id"]
                                                 fname = obj["file"]
                                                 answ_v = obj["answ_V"]
                                                 answ = obj["answ"] 
                                                 task = obj["_task"] 
                                                 tp = obj["_type"]      
                                                 #print (fname, answ_v, answ, idxx, task, tp)                
                                                 iop = cv2.imread(fname)
                                                 #LeoPost(fname, str(idxx))
                                 
                                                 s = base64.b64encode(imgbite(iop))
                                                 #print (s) 
                                                 obj = {"image":s.decode('ascii'), 
                                                        "answ_V": answ_v, 
                                                        "answ": answ,
                                                        "task": task,
                                                        "type":tp,
                                                        "_id": str(idxx),
                                                        "name": fname}
                                                 #print (obj["type"])
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
        for x in mgDC["4x4"]:
           J = list(new.posts.find({"task": x}))
           items[x] =len(J)
        self.render("upload.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))


class MainData(tornado.web.RequestHandler):
    def get(self):
       self.render("data.html", title="Нейронная сеть/Тренировка")



##
def LLK(i):
        aJNEW = {} 
        aJL = {}
        aJV = {} 
        for ix, x in enumerate(new.posts.find({ "_task": i})):
          if x["_type"] == 1:
            for k in list(x.keys())[3:]:
                
                if x[k]["answ_V"] == 1:
                     print (x[k]["file"],x[k]["answ_V"])
                     aJV[x[k]["file"].split("/")[-1]] = x[k]["answ_V"]
          else:
            if new.posts.find_one(x["_id"])["answ"] != []:
               aJNEW[ix] = new.posts.find_one(x["_id"])
               aJNEW[ix]["_id"] = str(aJNEW[ix]["_id"])
            if new.posts.find_one(x["_id"])["answ_L"] != []:
               aJL[ix] = new.posts.find_one(x["_id"])
               aJL[ix]["_id"] = str(aJL[ix]["_id"])
            if new.posts.find_one(x["_id"])["answ_V"] != []:
               aJV[ix] = new.posts.find_one(x["_id"])
               aJV[ix]["_id"] = str(aJV[ix]["_id"])

        return aJNEW, aJV, aJL
  

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
         self.file.write("{};answ_v:{};answ_l:{};answ_new_human:{};answ_human:{};task:{};\n".format(x["file"].split("/")[-1],
                                                                        [int(f) for f in x["answ_V"]],
                                                                        x["answ_L"],
                                                                        x["answ"],
                                                                        x["answ_H"],
                                                                        x["_task"])) 


def tardir(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file))




##
class MainLoad(tornado.web.RequestHandler):
    
    def get(self):
        items = {}
        for x in mgDC["4x4"]:
           J = list(new.posts.find({"_task": x}))
           #print (len(J))
           items[x] =len(J)
        self.render("load.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))
    def post(self):
        data_json = json.loads(self.request.body)
        if data_json["st"] == "prep":
                Gg = LLK(data_json["task"])
                #print "POST", len(Gg[0].keys()),len(Gg[1].keys()), len(Gg[2].keys())#self.request.body #Gg
                """Готовим статистику""" 
                kolo = {"answ":len(Gg[0].keys()) , "answ_L":len(Gg[2].keys()) , "answ_V":len(Gg[1].keys())} 
                self.write(kolo)
        else:
                #print data_json["task"]
                
                """create load"""
                rec = record('temp_csv/'+data_json["task"])
                #rec.toDown('temp/'+data_json["task"])
                for ix, x in enumerate(new.posts.find({ "_task": data_json["task"]})):
                   if x["_type"] == 1:
                   #print (x)
                     for k in list(x.keys())[3:]:
                
                       if x[k]["answ_V"] == 1:
                          #print (x[k]["file"],x[k]["answ_V"])
                          rec.save_one(x[k]["file"],x[k]["answ_V"])
                   else:
                       rec.save(x)
                         
                #kolo = {"csv":'temp_csv/'+data_json["task"]+'.csv' , "arch":'to_load/'+data_json["task"]+'.tar.gz' }
                kolo = {"csv":'temp_csv/'+data_json["task"]+'.csv'}
                self.write(kolo)





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
bd struct
новое бд - 
после созания 
"""


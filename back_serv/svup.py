# -*- coding: utf-8 -*-
#from GPUi import gg #YOLO
from pymongo import MongoClient
from tornado.escape import json_encode
from bson.objectid import ObjectId

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
                #self.file = {}
		path = "data/"+dir_name
                print "PARSING",path
		valid_images = [".jpg",".png"]
		for r, d, f in os.walk(path):
		    #print r, d, f
		    for file in f:
			if valid_images[0] in file or valid_images[1] in file:
			   #print os.path.join(r, file)
                           self.file[file.split(".")[0]] = [os.path.join(r, file)]
			if ".csv" in file:
			   self.csv = os.path.join(r, file)

def LeoPost(x, idx, task):
    url = "http://148.251.0.181:8084/"
    with open(x, "rb") as f:
            data = f.read()
            payload = {"image":data.encode("base64"), "id":idx, "key":"oru6SF9kasU0uljhid6P0wSoZBduX8nY", "type":task}
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


def deansw(x):
    s = []
    for ix, i in enumerate(x):
        #print ix, i
        if i == 1:
           s.append(ix+1)
    return s


class DB(object):
    def __init__(self):
        self.pyDB = MongoClient('localhost', 27017)
        self.db = self.pyDB.test_database  
        self.posts = self.db.posts  

new = DB()    

class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    myfile = 0
    seeidx = 0
    name = "" #traffic_lights4x4.tar.gz 
    ss = new.posts.find()
    tempID = 0    

    def track_progress(self, x):
       #print len(list(enumerate(x)))
       for member in x:
              #print member
              self.write_message(json.dumps({"Process": "load"}))
       

    def open(self):
        ImageWebSocket.clients.add(self)
        print("WebSocket opened from: " + self.request.remote_ip)


    def on_message(self, message):
        
                ms =  json.loads(message)
                if list(ms.keys())[0] == "Start":
                   """Начало загрузки"""

                   self.name = ms["Start"]["Name"]
                   #print self.name
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
                           #print "Process start", ms["task"]
                           lss = ["gz", "tar"]
                           if self.name.split(".")[-1] in lss:
                                   tar = tarfile.open("archiv/"+self.name, "r")
                                   tar.extractall("data/"+self.name, members=self.track_progress(tar))
                                   tar.close()
                                   #print "Process Arhive Done", self.name
                                   HD.parseIMG(self.name)
                           if self.name.split(".")[-1] == "zip":
                                   zip = ZipFile("archiv/"+self.name)
                                   zip.extractall("data/"+self.name)
                           
                                   HD.parseIMG(self.name)
                           for ixx, fx in enumerate(HD.file.keys()[:4]):
                                   
                                   file_n = HD.file[fx][0]
                                   try:
                                      answ_H = HD.file[fx][1]
                                   except IndexError:
                                      answ_H = ""
                                   #print file_n, ms["task"], int(ms["type"])
                                   iop = cv2.imread(file_n)
                                   answ_V = gg(iop, ms["task"], int(ms["type"]))
                                   #answ_L = LeoPost(file_n, str(ixx), ms["task"])
                                   #print answ_H, answ_L["text"] #answ_V[0]
                                   
                                   post = {"file": file_n, 
                                           "answ": "", "answ_H": answ_H, "type":ms["type"],
                                           "answ_L" : "", "answ_V": answ_V[0], "task":ms["task"]}
                                           #"answ": "", "answ_V": "", "task":ms["task"], "type":ms["type"]}
                                           #"answ_L" : answ_L["text"], "answ_V": "1", "task":ms["task"]}
                                   I = new.posts.insert_one(post).inserted_id

                           self.ss = new.posts.find()
                           self.write_message(json.dumps({"Process": "loaddone"}))


                if list(ms.keys())[0] == "SeeAllData":
                      if ms["SeeAllData"] == "ProcessNext":
                                      
                                      try:
                                          self.tempID = ObjectId(ms["idxx"])
                                          posttoCH = new.posts.find_one(ObjectId(ms["idxx"]))
                                          posttoCH["answ_V"] = deansw(ms["answ_v"])
                                          new.posts.update_one({"_id" : ObjectId(ms["idxx"])},
                                                                  {"$set": posttoCH}, upsert=True)
                                          posttoCH = new.posts.find_one(ObjectId(ms["idxx"]))
       
                                      except KeyError:
                                          pass
                  
                                      if new.posts.count() != 0:

                                              try:
                                                 obj = self.ss.next()
                                              except StopIteration:
                                                 self.ss.rewind()
                                                 obj = self.ss.next()    
                                              idxx = obj["_id"]
                                              fname = obj["file"]
                                              answ_v = obj["answ_V"]
                                              answ = obj["answ"] 
                                              task = obj["task"] 
                                              tp = obj["type"]      
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
        #self.render("load.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))
        self.render("upload.html", title="Нейронная сеть/Тренировка", items=json.dumps(items))


class MainData(tornado.web.RequestHandler):
    def get(self):
       self.render("data.html", title="Нейронная сеть/Тренировка")





app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", MainUpload),
        (r"/alldata", MainData),
        (r"/websocket", ImageWebSocket),
        (r"/(robots-AI.jpg)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(index.png)", tornado.web.StaticFileHandler, {'path':'./'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path':'./', 'default_filename': 'index.html'}),
    ])
app.listen(8800)


tornado.ioloop.IOLoop.current().start()



